import humanfriendly
import json
import os
import pathlib
import requests
import shutil
import sys
import vdf

if __name__ == "__main__":
	TotalSize = 0
	global CollectionID
	global ServerPath

	if len( sys.argv ) <= 1:
		CollectionID = input( "Collection ID parameter not specified. Please enter it now: " )
	else:
		CollectionID = sys.argv[1]

	if len( sys.argv ) >= 3:
		os.chdir( sys.argv[2] )

	if not os.path.exists( "srcds.exe" ) and not os.path.exists( "srcds_run" ):
		print( "ERROR: Script is not in root folder of server." )
		sys.exit()

	print( "Gathering collection info..." )
	url = "https://api.steampowered.com/ISteamRemoteStorage/GetCollectionDetails/v1/"
	data = { "collectioncount": "1", "publishedfileids[0]": CollectionID }
	collectionList = requests.post( url, data )

	j = json.loads( collectionList.text )
	children = j["response"]["collectiondetails"][0]["children"] if "children" in j["response"]["collectiondetails"][0] else None
	print( "Successfully fetched collection info." )

	if children is None:
		print( "ERROR: Collection was detected, but it contains no content. Make sure the collection is public and try again." )
		sys.exit()

	addonIDs = []
	for addon in children:
		addonIDs.append( addon["publishedfileid"] )

	print( "Scanning for unused files in the cache folder..." )
	for path, dirs, files in os.walk( "garrysmod/cache/srcds" ):
		for name in files:
			if os.path.splitext( name )[0] not in addonIDs:
				finalPath = os.path.join( path, name )
				TotalSize += os.path.getsize( finalPath )
				os.remove( finalPath )
				print( f"Removing addon {finalPath}" )

	print( "Scanning for unused files in the workshop folder..." )
	for path, dirs, files in os.walk( "steam_cache/content/4000" ):
		for name in dirs:
			if name not in addonIDs:
				finalPath = os.path.join( path, name )
				for file in pathlib.Path( finalPath ).rglob( '*' ):
					TotalSize += file.stat().st_size
				shutil.rmtree( finalPath )
				print( f"Removing addon {finalPath}" )

	acf = vdf.load( open( "steam_cache/appworkshop_4000.acf" ) )
	for id in acf["AppWorkshop"]["WorkshopItemsInstalled"]:
		if id not in addonIDs:
			del acf["AppWorkshop"]["WorkshopItemsInstalled"][id]
	for id in acf["AppWorkshop"]["WorkshopItemDetails"]:
		if id not in addonIDs:
			del acf["AppWorkshop"]["WorkshopItemDetails"][id]
	vdf.dump( acf, open( "steam_cache/appworkshop_4000.acf", "w" ), True )

	print( "Finished!" )
	print( f"Total storage saved: {humanfriendly.format_size( TotalSize )}" )
	input( "Press any key to continue..." )
