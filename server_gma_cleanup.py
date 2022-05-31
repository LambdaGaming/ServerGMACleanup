import json
import os
import requests
import sys

if __name__ == "__main__":
	TotalSize = 0

	if len( sys.argv ) <= 1:
		CollectionID = input( "Collection ID parameter not specified. Please enter it now: " )
	else:
		CollectionID = sys.argv[1]

	if not os.path.exists( "srcds.exe" ) and not os.path.exists( "srcds_run" ):
		print( "ERROR: Script is not in root folder of server." )
		sys.exit()

	print( "Gathering collection info..." )
	url = "https://api.steampowered.com/ISteamRemoteStorage/GetCollectionDetails/v1/"
	data = { "collectioncount": "1", "publishedfileids[0]": CollectionID }
	collectionList = requests.post( url, data )

	j = json.loads( collectionList )
	children = j["response"]["collectiondetails"][0]["children"] or None
	print( "Successfully fetched collection info." )

	if children is None:
		print( "ERROR: Collection was detected, but it contains no content. Make sure the collection is public and try again." )
		sys.exit()

	addonIDs = []
	for addon in children:
		addonIDs.append( addon["publishedfileid"] )

	print( "Scanning for unused files in the cache folder..." )
	for path, dirs, files in os.walk( "garrysmod/cache" ):
		if os.path.splitext( files )[0] not in addonIDs:
			TotalSize += os.path.getsize( files )
			os.remove( files )
			print( f"Removing addon {files}" )

	for path, dirs, files in os.walk( "steam_cache/content/4000" ):
		if dirs not in addonIDs:
			TotalSize += os.path.getsize( dirs )
			os.rmdir( dirs )
			print( f"Removing addon {dirs}" )
