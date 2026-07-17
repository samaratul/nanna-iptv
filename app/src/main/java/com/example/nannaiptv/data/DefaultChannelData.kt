package com.example.nannaiptv.data

object DefaultChannelData {
    val categories = listOf(
        Category(
            language = "Nepali",
            subCategories = listOf(
                SubCategory("Sports", listOf(
                    Channel("NTV Sports"), Channel("AP1 TV (Cricket)"), Channel("Himalaya TV Sports (occasional)"), Channel("DishHome Sports (IPTV)")
                )),
                SubCategory("Entertainment", listOf(
                    Channel("Kantipur TV", url = "https://ktvhdsg.ekantipur.com:8443/high_quality_85840165/hd/playlist.m3u8", logoUrl = "https://upload.wikimedia.org/wikipedia/en/thumb/d/d7/Kantipur_Television_logo.svg/512px-Kantipur_Television_logo.svg.png"), 
                    Channel("AP1 TV"), Channel("Himalaya TV"), Channel("Galaxy 4K"), 
                    Channel("Image Channel"), Channel("Sagarmatha TV"), Channel("NTV Plus"), Channel("Disha TV Nepal"), 
                    Channel("Janata TV"), Channel("Nepal 1"), Channel("TV Today"), Channel("Mero TV")
                )),
                SubCategory("Movies", listOf(
                    Channel("Filmy Plus"), Channel("Ramailo Chautari"), Channel("Action Cinema"), Channel("NTV Plus"), 
                    Channel("Kalika TV"), Channel("Mero Cinema (IPTV)"), Channel("DishHome Cinema"), Channel("Kanxa TV (Movie blocks)")
                )),
                SubCategory("Music", listOf(
                    Channel("Kantipur Gold"), Channel("Music Nepal TV"), Channel("Image Music"), Channel("Channel Nepal"), 
                    Channel("Beluga Music"), Channel("TV Today (Music)"), Channel("Avenues Music"), Channel("Sagarmatha Music")
                )),
                SubCategory("News", listOf(
                    Channel("Kantipur TV"), Channel("News 24"), Channel("Avenues TV"), Channel("NTV"), 
                    Channel("Himalaya TV"), Channel("AP1 TV"), Channel("ABC TV"), Channel("Image TV News"), 
                    Channel("Sagarmatha TV"), Channel("Kalika TV"), Channel("Galaxy 4K"), Channel("Janata TV"), 
                    Channel("Nepal 1"), Channel("Mountain TV"), Channel("Awaaz TV"), Channel("Terai TV")
                )),
                SubCategory("Lifestyle & Fashion", listOf(
                    Channel("Mero TV (Youth/Lifestyle)"), Channel("AP1 TV (Lifestyle shows)"), 
                    Channel("Kantipur Gold (Youth blocks)"), Channel("Galaxy 4K (Lifestyle segments)")
                )),
                SubCategory("Devotional", listOf(
                    Channel("Aastha Nepali"), Channel("Hindu TV Nepal"), Channel("NTV (Morning Pooja)"), 
                    Channel("Sagarmatha TV (Devotional blocks)"), Channel("Image Channel (Bhajans)")
                )),
                SubCategory("Others (Kids/Infotainment)", listOf(
                    Channel("NTV Janarjya"), Channel("Mero TV (Kids blocks)"), Channel("Kantipur TV (Infotainment)"), 
                    Channel("Himalaya TV (Documentaries)")
                ))
            )
        ),
        Category(
            language = "Hindi",
            subCategories = listOf(
                SubCategory("Sports", listOf(
                    Channel("Star Sports 1 Hindi"), Channel("Star Sports 2"), Channel("Sony Ten 1/2/3"), 
                    Channel("Sony Sports Ten 5"), Channel("Star Sports Select 1/2"), Channel("DD Sports"), 
                    Channel("Star Sports First"), Channel("Eurosport India"), Channel("1Sports")
                )),
                SubCategory("Entertainment", listOf(
                    Channel("Star Plus"), Channel("Sony TV"), Channel("Colors"), Channel("Zee TV"), 
                    Channel("Star Bharat"), Channel("SAB TV"), Channel("Dangal TV"), Channel("Sony Pal"), 
                    Channel("Zee Anmol"), Channel("Star Utsav"), Channel("Colors Rishtey"), Channel("&TV"), 
                    Channel("Big Magic"), Channel("Ishara TV")
                )),
                SubCategory("Movies", listOf(
                    Channel("Star Gold"), Channel("Sony Max"), Channel("Zee Cinema"), Channel("Colors Cineplex"), 
                    Channel("&pictures"), Channel("Star Gold 2"), Channel("Sony Wah"), Channel("Zee Action"), 
                    Channel("Zee Classic"), Channel("Movies Now 2"), Channel("&xplor HD"), Channel("Star Suvarna (Dubbed)")
                )),
                SubCategory("Music", listOf(
                    Channel("MTV Beats"), Channel("9XM"), Channel("B4U Music"), Channel("Zoom TV"), 
                    Channel("Music India"), Channel("Mastiii"), Channel("Zing"), Channel("Sony Mix"), Channel("Bindass")
                )),
                SubCategory("News", listOf(
                    Channel("Aaj Tak"), Channel("ABP News"), Channel("NDTV India"), Channel("India TV"), 
                    Channel("Zee News"), Channel("Republic Bharat"), Channel("CNN News18"), Channel("News18 India"), 
                    Channel("TV9 Bharatvarsh"), Channel("Times Now Navbharat"), Channel("DD National"), Channel("DD News")
                )),
                SubCategory("Lifestyle & Fashion", listOf(
                    Channel("TLC (Hindi feed)"), Channel("NDTV Good Times"), Channel("HGTV India"), 
                    Channel("Food Food"), Channel("Travel XP"), Channel("Green TV")
                )),
                SubCategory("Devotional", listOf(
                    Channel("Aastha TV"), Channel("Sanskar TV"), Channel("Disha TV"), Channel("Paras TV"), 
                    Channel("Zee Jagran"), Channel("Ishwar TV"), Channel("God TV (Hindi)")
                )),
                SubCategory("Others (Kids/Infotainment)", listOf(
                    Channel("Cartoon Network Hindi"), Channel("Pogo TV"), Channel("Disney Channel Hindi"), 
                    Channel("Hungama TV"), Channel("Nickelodeon India"), Channel("Sony Yay!"), 
                    Channel("Discovery Kids"), Channel("Nat Geo Kids (Hindi)")
                ))
            )
        ),
        Category(
            language = "English",
            subCategories = listOf(
                SubCategory("Sports", listOf(
                    Channel("Star Sports 1 (English)"), Channel("Sony Sports Ten 1/3/4"), Channel("Eurosport"), 
                    Channel("Star Sports Select 1/2"), Channel("Premier Sports"), Channel("Sky Sports (via IPTV)"), 
                    Channel("Sony Sports Ten 5")
                )),
                SubCategory("Entertainment", listOf(
                    Channel("Zee Cafe"), Channel("Star World"), Channel("Colors Infinity"), Channel("Comedy Central"), 
                    Channel("Star World Premiere"), Channel("Romedy Now"), Channel("FX"), Channel("AXN"), Channel("Warner TV")
                )),
                SubCategory("Movies", listOf(
                    Channel("HBO", url = "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8", logoUrl = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/de/HBO_logo.svg/512px-HBO_logo.svg.png"), 
                    Channel("Star Movies"), Channel("Sony Pix"), Channel("Movies Now"), 
                    Channel("Warner TV"), Channel("Star Movies Select"), Channel("&Flix"), Channel("Movies Now 2"), 
                    Channel("MGM HD"), Channel("TCM")
                )),
                SubCategory("Music", listOf(
                    Channel("VH1 India"), Channel("MTV India (English blocks)"), Channel("9XO (if available via IPTV)"), 
                    Channel("MTV Live HD")
                )),
                SubCategory("News", listOf(
                    Channel("BBC World News", url = "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8", logoUrl = "https://upload.wikimedia.org/wikipedia/commons/thumb/6/62/BBC_News_2019.svg/512px-BBC_News_2019.svg.png"), 
                    Channel("CNN International", url = "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8", logoUrl = "https://upload.wikimedia.org/wikipedia/commons/thumb/6/66/CNN_International_logo.svg/512px-CNN_International_logo.svg.png"), Channel("Al Jazeera English"), 
                    Channel("NDTV 24x7"), Channel("Republic World"), Channel("Times Now"), Channel("CNN-News18"), 
                    Channel("DW News"), Channel("France 24"), Channel("RT News"), Channel("Sky News"), Channel("ABC Australia")
                )),
                SubCategory("Lifestyle & Fashion", listOf(
                    Channel("TLC"), Channel("Fashion TV (FTV)"), Channel("Discovery Travel & Living"), 
                    Channel("Nat Geo People"), Channel("HGTV"), Channel("Food Network"), Channel("Love Nature")
                )),
                SubCategory("Devotional", listOf(
                    Channel("God TV (English Christian channel)"), Channel("Faith World TV")
                )),
                SubCategory("Others (Kids/Infotainment)", listOf(
                    Channel("Cartoon Network", logoUrl = "https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Cartoon_Network_2010_logo.svg/512px-Cartoon_Network_2010_logo.svg.png"), 
                    Channel("Disney Channel"), Channel("Discovery Channel"), 
                    Channel("National Geographic"), Channel("Animal Planet"), Channel("Nat Geo Wild"), 
                    Channel("Nick HD+"), Channel("Baby TV"), Channel("Discovery Science"), 
                    Channel("History TV18"), Channel("Sony BBC Earth")
                ))
            )
        ),
        Category(
            language = "Bhojpuri",
            subCategories = listOf(
                SubCategory("Sports", listOf()), // No dedicated channels
                SubCategory("Entertainment", listOf(
                    Channel("Mahuaa TV"), Channel("Dabangg TV"), Channel("Bhojpuri Dhamaka"), Channel("Mahuaa Plus"), 
                    Channel("Oscar TV"), Channel("Bhojpuri Express"), Channel("Bhojpuri Star")
                )),
                SubCategory("Movies", listOf(
                    Channel("Bhojpuri Cinema"), Channel("Filmy Bhojpuri"), Channel("Dabangg Cinema"), 
                    Channel("Mahuaa Cinema"), Channel("B4U Bhojpuri"), Channel("Bhojpuri Star Cinema")
                )),
                SubCategory("Music", listOf(
                    Channel("Mahuaa Music"), Channel("B4U Bhojpuri"), Channel("Sangeet Bhojpuri"), 
                    Channel("Bhojpuri Music TV"), Channel("Big Ganga (Bhojpuri/Jharkhand music & culture)")
                )),
                SubCategory("News", listOf()), // No dedicated channels
                SubCategory("Lifestyle & Fashion", listOf()), // No dedicated channels
                SubCategory("Devotional", listOf(
                    Channel("Aastha TV (Hindi, heavily watched)"), Channel("Disha TV"), Channel("Sanskar TV"), 
                    Channel("local Bhojpuri devotional blocks on Mahuaa TV")
                )),
                SubCategory("Others (Kids)", listOf()) // Primarily use Hindi kids channels
            )
        )
    )

    // Helper to get flattened categories for the sidebar
    // e.g. "🇳🇵 Nepali - Sports" -> List<Channel>
    val flattenedCategories: Map<String, List<Channel>> by lazy {
        val map = mutableMapOf<String, List<Channel>>()
        categories.forEach { category ->
            category.subCategories.forEach { subCategory ->
                if (subCategory.channels.isNotEmpty()) {
                    val flattenedName = "${category.language} - ${subCategory.genre}"
                    map[flattenedName] = subCategory.channels
                }
            }
        }
        map
    }
}
