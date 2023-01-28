# Server GMA Cleanup
 Python script to detect and remove unused downloaded addons from Gmod servers to free up space. Requires Python 3.6+ as well as the `requests`, `humanfriendly`, and `vdf` modules. This should work on both Windows and Linux, although Linux support is currently untested.
 The script works by comparing addons in a specified workshop collection against the files located in the `garrysmod/cache/srcds` and `steam_cache/content/4000` folders. Any addons found that are not in the collection will be removed. The script also removes addon entries from the `appworkshop_4000.acf` file to prevent errors while downloading a previously deleted addon.

## Usage
 This script takes two arguments: Workshop collection ID and file path to the root directory of the server. If an argument isn't specified, it will prompt the user for it before continuing.

## Notes
- The specified workshop collection MUST be set to public. Setting the collection to unlisted won't work as the Steam web API will return an empty list.
- This only works on dedicated servers that use a workshop collection to automatically download addons. If you need to cleanup unused addons for the actual game, use the `menu_cleanupgmas` console command.
