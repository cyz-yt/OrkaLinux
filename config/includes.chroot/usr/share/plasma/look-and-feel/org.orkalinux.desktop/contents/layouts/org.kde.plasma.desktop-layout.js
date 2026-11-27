var panel = new Panel
panel.location = "bottom"
panel.height = 2 * Math.floor(gridUnit * 2.5 / 2)
panel.floating = true

var kickoff = panel.addWidget("org.kde.plasma.kickoff")
kickoff.currentConfigGroup = ["General"]
kickoff.writeConfig("icon", "orka-start")
kickoff.writeConfig("primaryActions", 2)
kickoff.writeConfig("systemFavorites", ["reboot", "shutdown"])

var wanted = ["org.kde.dolphin.desktop", "firefox.desktop", "discord.desktop",
              "kitty.desktop", "com.spotify.Client.desktop"]
var launchers = []
for (var i = 0; i < wanted.length; i++) {
    if (applicationExists(wanted[i])) {
        launchers.push("applications:" + wanted[i])
    }
}
var tasks = panel.addWidget("org.kde.plasma.icontasks")
tasks.currentConfigGroup = ["General"]
tasks.writeConfig("launchers", launchers)

panel.addWidget("org.kde.plasma.marginsseparator")
panel.addWidget("org.kde.plasma.systemtray")
panel.addWidget("org.kde.plasma.digitalclock")
panel.addWidget("org.kde.plasma.showdesktop")

var desktopsArray = desktopsForActivity(currentActivity());
for (var j = 0; j < desktopsArray.length; j++) {
    desktopsArray[j].wallpaperPlugin = "org.kde.image";
    desktopsArray[j].currentConfigGroup = ["Wallpaper", "org.kde.image", "General"];
    desktopsArray[j].writeConfig("Image", "file:///usr/share/desktop-base/orkalinux-theme/wallpaper/");
}
