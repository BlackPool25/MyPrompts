SOURCE: Improving Testing Prompt.pdf, Page 134
TYPE: User Prompt
================================================================================

I want an agent for setting up this is my self hosted enviroment give me a good prompt for an 
agent that will read the markdown file I tell about the chat I had with an AI about the setup and 
come up with a plan using the best named techniques and before that always use context7 mcp 
and websearch to ensure no outdated setups and best approaches and no over complicating it and 
best quality streaming. 
Use **Jellyfin + Sonarr + Radarr + Prowlarr + qBittorrent**, with optional hardware transcoding on 
a supported GPU. Jellyfin supports Docker deployment and hardware-accelerated transcoding on 
supported Intel, AMD, NVIDIA, Apple, and Rockchip hardware. Sonarr monitors RSS feeds for 
episodes, grabs/sorts/renames them, and can upgrade file quality later. Radarr does the same for 
movies. Prowlarr acts as the central indexer manager/proxy for torrent trackers and Usenet 
indexers, so you do not configure indexers separately in each app. qBittorrent is a torrent client 
with a Web UI and remote control. ([Jellyfin][1])
A clean split for your stack is:
* **Jellyfin** for playback and library access. Use its official Android and Android TV clients for 
phones and TVs. ([Jellyfin][2])
* **Sonarr** for TV and anime. It is the automation layer for episodes and quality upgrades. 
([GitHub][3])
* **Radarr** for movies. It manages movie search, downloads, sorting, and upgrades. 
([radarr.video][4])
* **Prowlarr** as the single indexer manager for both Sonarr and Radarr. ([Servarr Wiki][5])
* **qBittorrent** as the download client, kept private on your internal Docker network. 
([qbittorrent.org][6])
For your architecture, I would keep the media stack on a dedicated Docker network and expose 
only **Jellyfin** through NGINX/Cloudflare Tunnel. Leave **Sonarr, Radarr, Prowlarr, and 
qBittorrent** private. Then mount one shared downloads path and one shared media path into all 
of them so file moves and imports stay consistent. That is the least messy layout for your use case.
If you have a decent GPU or Intel iGPU, turn on Jellyfin hardware transcoding. That matters more 
than almost any other "upgrade" because it improves playback for remote devices, weak clients, 
and codec conversion. ([Jellyfin][7])
For your setup, the practical answer is: **Jellyfin + Sonarr + Radarr + Prowlarr + qBittorrent**, with 
GPU transcoding if available, and no extra auth layer in front of Jellyfin unless you have a separate 
reason to restrict access.
[1]: https://jellyfin.org/docs/general/installation/container/?utm_source=chatgpt.com "Container"
[2]: https://jellyfin.org/downloads/?utm_source=chatgpt.com "Clients"
[3]: https://github.com/Sonarr/Sonarr?utm_source=chatgpt.com "Sonarr/Sonarr: Smart PVR for 
newsgroup and bittorrent ..."
[4]: https://radarr.video/?utm_source=chatgpt.com "Radarr"
[5]: https://wiki.servarr.com/prowlarr?utm_source=chatgpt.com "Prowlarr | Servarr Wiki"
[6]: https://www.qbittorrent.org/?utm_source=chatgpt.com "qBittorrent Official Website"
[7]: https://jellyfin.org/docs/general/administration/hardware-selection/?utm_source=chatgpt.com 
"Selecting Appropriate Hardware"
