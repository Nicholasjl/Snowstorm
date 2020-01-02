SnowStorm 

---
THIS PROGRAM IS DRAW LESSON FROM [GOLDENEYE](https://github.com/jseidl/GoldenEye)


================

SnowStorm is an python app for SECURITY TESTING PURPOSES ONLY!

SnowStorm is a HTTP DoS Test Tool. 
Using asyncio to make it faster and lighter.
Attack Vector exploited: HTTP Keep Alive + NoCache

Yep,it can be called GoldenEye-asyncio

Usage
-----------------------------------------------------------------------------------------------------------
     Uusage: SnowStorm.py [-h] -u URL [-m {get,post,random}] [-c COROS] [-w WORKERS] [-d [DEBUG]] [--no-payload [NO_PAYLOAD]] [-n [NOSSLCHECK]] [-a [AGENT]]

    
     OPTIONS:
         Flag           Description                     Default
         -u, --url      the website you want fight
         -c, --coros      Number of concurrent Coroutines peer process                (default: 1000)
         -w, --worker   Number of Processes                                           (default: 10)
         -m, --method       HTTP Method to use 'get' or 'post'  or 'random'           (default: get)
         -d, --debug        Enable Debug Mode [more verbose output]                   (default: False)
         -h, --help     Shows this help
         -n, --nosslcheck no ssl check                                                (default:False)
         -a --agent the file for useragent(can find at res/list/useragents)           (default:None)
         --no-payload  Don't use headers                                              (default:False)

Changelog
-----------------------------------------------------------------------------


License
-----------------------------------------
This software is distributed under the GNU General Public License version 3 (GPLv3)

LEGAL NOTICE
-----------------------------------------
THIS SOFTWARE IS PROVIDED FOR EDUCATIONAL USE ONLY! IF YOU ENGAGE IN ANY ILLEGAL ACTIVITY THE AUTHOR DOES NOT TAKE ANY RESPONSIBILITY FOR IT. BY USING THIS SOFTWARE YOU AGREE WITH THESE TERMS.


THIS PROGRAM IS DRAW LESSON FROM GOLDENEYE
