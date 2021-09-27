# NPR's Ask Me Another - Complete Feed

Ask Me Another was a fantastic trivia quiz show on NPR, which has sadly been cancelled. While all of the episodes are still [available online](https://www.npr.org/programs/ask-me-another/archive), the official podcast feed has always dropped older episodes as time has gone on, which means that these episodes can't easily be listened to in podcast apps.

I have gone back through snapshots of the podcast feed from the excellent Internet Archive ([here for the oldest episodes](https://web.archive.org/web/*/www.npr.org/rss/podcast.php?id=510299) and [here to the present](https://web.archive.org/web/*/feeds.npr.org/510299/podcast.xml)), extracted all podcast entries back to the beginning, and assembled them into one complete podcast feed, as if the old entries had never been removed. (This does mean that episode entries that were *intentionally* removed and replaced with a fixed version are also present. If the same episode appears multiple times, that's probably what happened.)

[Subscribe to the feed with this URL](https://jbiatek.github.io/AskMeAnotherCompleteFeed/ama_complete_feed.xml).

All of the actual audio links are untouched, since as of September 2021 they appear to still be good. If NPR does ever decide to move or delete these files, then this feed will break. I'm providing *just the feed* as an archive and index of media that was already public.

## Technical notes

The script used to extract the items is in this repository as well, if you're interested. I used the Ruby gem `wayback_machine_downloader` to grab all of the archived feeds. The `<guid>` tags for items seemed to be relatively reliable, so the script trusted that as a key, taking the latest available `<item>` tag for each GUID. At some points, it looks like some Microsoft Word XML got in to the file which caused parse errors, so I filtered those out after ensuring that a correct version of each one also existed. In addition, there is one particular CDN that does appear to no longer work, so that was also filtered out after verifying that the same content was available with working links elsewhere.
