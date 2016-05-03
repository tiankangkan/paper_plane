#!/bin/sh

# 0 0,12 * * * * /bin/sh /data/project/paper_plane/run_spider.sh
# 0 0,12 * * * * /bin/sh /Users/kangtian/Documents/Master/paper_plane/run_spider.sh


cd /data/project/paper_plane/king_spider/
for var in "LuoWangJournal" "LuoWangEssays" "YiKeEssays" ; do
    echo "scrapy crawl: $var"
    scrapy crawl $var
done

