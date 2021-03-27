'''INFO
Name:        xetch
Description: Fetches system information with a Python script
Author(s):   Robert Furr (Initial command set commit), B00bleaTea (xetch creator and maintainer)
Year:        2021

This and all other command sets are licensed under the GNU General Public License, see the LICENSE file included with DSAK for details.'''
import re, subprocess, getpass, socket, time, shutil, sys
from dsaklib.appmodules.colorama import Fore, Style
import dsaklib.appmodules.psutil as psutil
def run_xetch(args=None,artName=None):
  # NOTE: Fix 'args' so you can actually get args to work like the CLI version
  if args == None:
    args = 'n/a'
  '''Runs xetch.'''
  # Also please for the love of god B00bleaTea, use 2 space imdemts. It would make my life much easier.

  # -*- coding: utf-8 -*-

  # ~*~ art by      : https://roly.neocities.org/ ~*~
  # ~*~ code by     : https://acactusinpain.neocities.org/ ~*~
  # ~*~ github repo : https://github.com/B00bleaTea/xetch ~*~

  #import re, subprocess, getpass, socket, dsaklib.appmodules.psutil, time, shutil, sys
  #from dsaklib.appmodules.colorama import Fore, Style

  # variables, functions and constants

  ## info ##
  __date__    = "2021/03/14"
  __update__  = "2021/03/20"
  __author__  = "B00bleaTea"
  __credits__ = ["https://roly.neocities.org/",
                "https://github.com/robtech21/",
                "https://github.com/tempora/"]
  ########


  def get_packages():
      # defining the ways you can list installed packages
      # xx || yy = do xx, if xx fails do yy
      pac_mans = ["apk info",
                  "pacman -Q",
                  "dpkg -l",
                  "yum list installed",
                  "dnf list installed",
                  "repoquery -a --installed",
                  "zypper se --installed-only",
                  "rpm -qa",
                  "brew list",
                  "flatpak list",
                  "snap list",
                  "equery list \"*\"",
                  "xbps-query -l",
                  "pkg_info",
                  "pkg info",
                  "eopkg list-installed",
                  "scratchpkg listinst",
                  "nix-env -qa --installed \"*\"",
                  "swupd bundle-list --status",
                  "omf list",
                  "omz list"]
      # default value is empty
      package_managers = []
      # default string
      packager = ''
      # package count
      pac_cnt = 0
      # looping and trying
      for pac in pac_mans:
          try:
              installed_package_count = subprocess.check_output(pac.split(), shell=False).decode().split('\n')
              package_managers.append((pac.replace('-', ' ').split()[0],
                                      len(installed_package_count)))
          # if command failed
          except (FileNotFoundError, subprocess.CalledProcessError):
              pass
          # if any package managers found
      if package_managers:
          for pcm in package_managers:
              pac_cnt += pcm[1]
              # the the first and second elements of the tuple and place it inside a string
              packager += f'{pcm[0]} ({pcm[1]}), '
          # packager = package without the last 2 characters(", ")
          packager = packager[:-2]
          # return the package manager string and the package count
          return packager, pac_cnt
      # if no package manager found, return "none"
      return None, None


  # calculate percentage
  def calc_percentage(used: (int, float), total: (int, float)):
      try:
          return round((used * 100) / total)
      except (ZeroDivisionError, PermissionError, TypeError):
          return 0


  # prepare art for use in the Art.art function
  def make_art(art: str, delimiter: str = '*'):
      return art.replace(delimiter, '').split('\n')


  STR_NONE = (str, None)
  INT_NONE = (int, None)
  FLOAT_INT_NONE = (float, int, None)
  # the colour palate for xetch, can be edited to your taste
  # use unicode escape sequences to have custom colours
  COLOUR_PALATE = {
      "logo": Fore.CYAN,
      "main_text": Fore.BLUE,
      "user_at": Fore.YELLOW,
      "normal_text": Style.RESET_ALL,
      "white_text": Fore.WHITE,
      "light_blue": Fore.LIGHTBLUE_EX,
      "magenta_purple": Fore.LIGHTMAGENTA_EX,
      "magenta": Fore.MAGENTA,
      "orange": Fore.LIGHTRED_EX,
      "light_green": Fore.LIGHTGREEN_EX,
      "gold": Fore.LIGHTYELLOW_EX,
      "red": Fore.RED,
      "green": Fore.GREEN,
      "reset_all": Style.RESET_ALL,
      "light_red": Fore.LIGHTRED_EX
  }

  # finding all specs of the system
  try:
      username = getpass.getuser()
      hostname = socket.gethostname()
  except (PermissionError, Exception) as e:
      print(f'{COLOUR_PALATE["red"]}[DEBUG] user error - {e}{COLOUR_PALATE["reset_all"]}')
      username, hostname = (None, None)
  try:
      kernel = subprocess.check_output(['uname', '-r']).decode().strip()
  except (FileNotFoundError, PermissionError) as e:
      print(f'{COLOUR_PALATE["red"]}[DEBUG] kernel error - {e}{COLOUR_PALATE["reset_all"]}')
      kernel = None
  system_uptime = time.gmtime(time.time() - psutil.boot_time())
  system_uptime = f"{system_uptime.tm_hour}h {system_uptime.tm_min}m {system_uptime.tm_sec}s"
  pacs = get_packages()
  # >> is a bitwise shift, shifting the values to get the values in
  # the measurement we want
  try:
      ram_total = psutil.virtual_memory().total >> 20
      ram_used = psutil.virtual_memory().used >> 20
  except (PermissionError, FileNotFoundError) as e:
      print(f'{COLOUR_PALATE["red"]}[DEBUG] ram error - {e}{COLOUR_PALATE["reset_all"]}')
      ram_used, ram_total = (0, 0)
  try:
      disk_total = shutil.disk_usage('/').total >> 30
      disk_used = shutil.disk_usage('/').used >> 30
  except (PermissionError, FileNotFoundError) as e:
      print(f'{COLOUR_PALATE["red"]}[DEBUG] disk error - {e}{COLOUR_PALATE["reset_all"]}')
      disk_total, disk_used = (0, 0)

  # the path to the os-release file
  os_release_file = "/etc/os-release"


  class Art:
      @classmethod
      def art(cls, user: STR_NONE, host: STR_NONE,
              os: STR_NONE, kernels: STR_NONE, uptime: STR_NONE,
              package: STR_NONE, package_count: INT_NONE, total_root: INT_NONE,
              used_root: INT_NONE, total_ram: FLOAT_INT_NONE,
              used_ram: FLOAT_INT_NONE, art: list[str]):
          art = f'''
  {art[0]}{user}{COLOUR_PALATE["user_at"]}@{COLOUR_PALATE["normal_text"]}{host}
  {COLOUR_PALATE["logo"]}{art[1]}{COLOUR_PALATE["main_text"]}os       | {COLOUR_PALATE["normal_text"]}{os}
  {COLOUR_PALATE["logo"]}{art[2]}{COLOUR_PALATE["main_text"]}kernel   | {COLOUR_PALATE["normal_text"]}{kernels}
  {COLOUR_PALATE["logo"]}{art[3]}{COLOUR_PALATE["main_text"]}uptime   | {COLOUR_PALATE["normal_text"]}{uptime}
  {COLOUR_PALATE["logo"]}{art[4]}{COLOUR_PALATE["main_text"]}packages | {COLOUR_PALATE["normal_text"]}{package} [{package_count}]
  {COLOUR_PALATE["logo"]}{art[5]}{COLOUR_PALATE["main_text"]}/ usage  | {COLOUR_PALATE["normal_text"]}{used_root}/{total_root}GB [{calc_percentage(used_root, total_root)}%]
  {COLOUR_PALATE["logo"]}{art[6]}{COLOUR_PALATE["main_text"]}memory   | {COLOUR_PALATE["normal_text"]}{used_ram}/{total_ram}MB [{calc_percentage(used_ram, total_ram)}%]
  '''
          return art[art.find('\n') + 1:art.rfind('\n')]


  try:
      with open(os_release_file, 'r') as f:
          # the pattern to find the distro name
          pattern = re.compile(r"^[nN][aA][mM][eE]=.+")
          distro = f.read()
          # finding NAME= and removing it, leaving up with the distro only
          distro = pattern.search(distro).group()[5:].replace('"', '')
  # in file doesn't exist
  except FileNotFoundError:
      try:
          # giving os_release_file a new value
          os_release_file = '/usr/lib/os-release'
          with open(os_release_file, 'r') as f:
              # the pattern to find the distro name
              pattern = re.compile(r"^[nN][aA][mM][eE]=.+")
              distro = f.read()
              # finding NAME= and removing it, leaving up with the distro only
              distro = pattern.search(distro).group()[5:].replace('"', '')
      # if that file doesn't exist
      except FileNotFoundError:
          # find the type of their os
          try:
              distro = subprocess.check_output(['uname', '-s']).decode().strip()
          except (FileNotFoundError, subprocess.CalledProcessError):
              distro = 'unknown'


  # ] is just a way of showing the boundaries
  # :) = tested, ? = not tested
  art_list = {
      # default :)
      "linux": make_art(f'''          ]
    {COLOUR_PALATE["white_text"]}.~.     ]
    {COLOUR_PALATE["white_text"]}/{COLOUR_PALATE["gold"]}V{COLOUR_PALATE["white_text"]}\\     ]
  {COLOUR_PALATE["white_text"]}// \\\\    ]
  {COLOUR_PALATE["white_text"]}/(   )\\   ]
  {COLOUR_PALATE["gold"]}^`~'^    ]
  {COLOUR_PALATE["light_blue"]}         ]''', ']'),

      # arco :)
      "arcolinux": make_art(f'''                ]
        __       ]
      ----      ]
      ------     ]
    --------    ]
    ----  {COLOUR_PALATE["white_text"]}==={COLOUR_PALATE["logo"]}-   ]
  ---     {COLOUR_PALATE["white_text"]}=={COLOUR_PALATE["logo"]}--  ]'''[1:], ']'),

      # arch :)
      "arch linux": make_art(f'''               ]
        {COLOUR_PALATE["main_text"]},        ]
      {COLOUR_PALATE["main_text"]},,,       ]
      {COLOUR_PALATE["main_text"]},,,{COLOUR_PALATE["logo"]},,      ]
    ,,,,,,,     ]
    .,*   *,.    ]
  .,       ,.   ]''', ']'),

      # alpine :)
      "alpine linux": make_art(f'''                               ]
        {COLOUR_PALATE["white_text"]},..                     ]
      {COLOUR_PALATE["white_text"]}..   ,,      ..           ]
      {COLOUR_PALATE["white_text"]},,     .,   ..  ,,         ]
    {COLOUR_PALATE["white_text"]},,*       ,,.      ,.       ]
    {COLOUR_PALATE["white_text"]}.,*'*       ..       .,      ]
  {COLOUR_PALATE["white_text"]},.**'**       ''        ..    ]''', ']'),

      # artix :)
      "artix linux": make_art(f'''               ]
        {COLOUR_PALATE["light_blue"]},        ]
      {COLOUR_PALATE["light_blue"]},',       ]
      {COLOUR_PALATE["light_blue"]},,,,,      ]
                ]
    {COLOUR_PALATE["logo"]}.,*   *,.    ]
  {COLOUR_PALATE["logo"]}.,       ,.   ]''', ']'),

      # debian :)
      "debian gnu/linux": make_art(f'''                ]
    {COLOUR_PALATE["magenta_purple"]}/&&&&&*&\\     ]
  {COLOUR_PALATE["magenta_purple"]},&   .-.  &'   ]
    {COLOUR_PALATE["magenta_purple"]}&. |     [    ]
    {COLOUR_PALATE["magenta_purple"]}&   .___=     ]
    {COLOUR_PALATE["magenta_purple"]}\\&            ]
      {COLOUR_PALATE["magenta_purple"]}\\*          ]''', ']'),

      # endeavour :)
      "endeavouros": make_art(f'''                 ]
      {COLOUR_PALATE["orange"]}/  \\\\       ]
      {COLOUR_PALATE["orange"]}/ {COLOUR_PALATE["magenta"]}/``{COLOUR_PALATE["magenta_purple"]}\\\\      ]
    {COLOUR_PALATE["orange"]}/ {COLOUR_PALATE["magenta"]}/````{COLOUR_PALATE["magenta_purple"]}\\\\    ] 
  {COLOUR_PALATE["orange"]}/ {COLOUR_PALATE["magenta"]}-`````_) {COLOUR_PALATE["magenta_purple"]}\\    ]
  {COLOUR_PALATE["orange"]}/{COLOUR_PALATE["magenta"]}_-___`` {COLOUR_PALATE["magenta_purple"]}__=    ]
    {COLOUR_PALATE["orange"]}/={COLOUR_PALATE["magenta"]}====={COLOUR_PALATE["magenta_purple"]}--      ]''', ']'),

      # manjaro :)
      "manjaro linux": make_art(f'''              ]
  {COLOUR_PALATE["light_green"]}:::::: ::    ]
  {COLOUR_PALATE["light_green"]}:: ;;; ::    ]
  {COLOUR_PALATE["light_green"]}:: ;;; ::    ]
  {COLOUR_PALATE["light_green"]}:: ;;; ::    ]
  {COLOUR_PALATE["light_green"]}:: ;;; ::    ]
  {COLOUR_PALATE["light_green"]}:: ;;; ::    ]''', ']'),

      # elementary :)
      "elementary os": make_art(f'''                ]
    {COLOUR_PALATE["light_blue"]}a&&&&a       ]
    {COLOUR_PALATE["light_blue"]}'   a. '      ]
  {COLOUR_PALATE["light_blue"]}&  &  &  &     ]
  {COLOUR_PALATE["light_blue"]}&  &  &  &     ]
    {COLOUR_PALATE["light_blue"]}._ a'_ .      ]
    {COLOUR_PALATE["light_blue"]}*&&&&*       ]''', ']'),

      # ubuntu :)
      "ubuntu": make_art(f'''               ]
          {COLOUR_PALATE["orange"]}_      ]
      {COLOUR_PALATE["orange"]}---(_)     ]
  {COLOUR_PALATE["orange"]}_/  ---  \\\\   ]
  {COLOUR_PALATE["orange"]}(_) |   |      ]
  {COLOUR_PALATE["orange"]}\\\\  --- _/    ]
    {COLOUR_PALATE["orange"]}---(_)      ]''', ']'),

      # gentoo :)
      "gentoo": make_art(f'''              ]
  {COLOUR_PALATE["magenta_purple"]}_-----__     ]
  {COLOUR_PALATE["magenta_purple"]}(       \\\\   ]
  {COLOUR_PALATE["magenta_purple"]}\\\\   0  \\\\   ]
    {COLOUR_PALATE["magenta_purple"]}\\\\     )    ]
  {COLOUR_PALATE["magenta_purple"]}(     _/     ]
  {COLOUR_PALATE["magenta_purple"]}\\\\____/      ]''', ']'),

      # linux lite ?
      "linux lite": make_art(f'''            ]
    {COLOUR_PALATE["gold"]},         ]
  {COLOUR_PALATE["gold"]}"\\",       ]
  {COLOUR_PALATE["gold"]}"=\\=",     ]
    {COLOUR_PALATE["gold"]}"=\\=",    ]
    {COLOUR_PALATE["gold"]}"-\\-"    ]
        {COLOUR_PALATE["gold"]}\\     ]''', ']'),

      # solaris ?
      "solaris": make_art(f'''                               ]
      {COLOUR_PALATE["gold"]}..`,,``..``.`..`          ]
    {COLOUR_PALATE["gold"]}`.`,.          ``..`        ]
    {COLOUR_PALATE["gold"]}.`.`               ``.`      ]
  {COLOUR_PALATE["gold"]}..`.                 ``.      ]
  {COLOUR_PALATE["gold"]}.`.`                  ``,`    ]
  {COLOUR_PALATE["gold"]}`.`                   ``.`    ]''', ']'),

      # slackware :)
      "slackware": make_art(f'''                    ]
        {COLOUR_PALATE["light_blue"]}x  x          ]
    {COLOUR_PALATE["light_blue"]}x   ___  x       ]
  x   / __|    x     ]
  {COLOUR_PALATE["main_text"]}x   \\__ \\    x     ]
    {COLOUR_PALATE["main_text"]}x  |___/ x       ]
        {COLOUR_PALATE["main_text"]}x  x          ]''', ']'),

      # openSUSE :)
      "opensuse": make_art(f'''                     ]
  {COLOUR_PALATE["light_green"]}___|⎻⎻⎻⎻⎻⎻⎻\\_       ]
  {COLOUR_PALATE["light_green"]}     ---     \\_     ]
  {COLOUR_PALATE["light_green"]}     | *|     |     ]
  {COLOUR_PALATE["light_green"]}     ⎻⎻⎻       |    ]
  {COLOUR_PALATE["light_green"]}        ____/⎻      ]
  {COLOUR_PALATE["light_green"]}⎻⎻⎻⎻⎻⎻⎻             ]''', ']'),
      "opensuse leap": make_art(f'''                     ]
  {COLOUR_PALATE["light_green"]}___|⎻⎻⎻⎻⎻⎻⎻\\_       ]
  {COLOUR_PALATE["light_green"]}     ---     \\_     ]
  {COLOUR_PALATE["light_green"]}     | *|     |     ]
  {COLOUR_PALATE["light_green"]}     ⎻⎻⎻       |    ]
  {COLOUR_PALATE["light_green"]}        ____/⎻      ]
  {COLOUR_PALATE["light_green"]}⎻⎻⎻⎻⎻⎻⎻             ]''', ']'),

      # fedora :)
      "fedora": make_art(f'''           ]
  {COLOUR_PALATE["main_text"]}  __      ]
  {COLOUR_PALATE["main_text"]} / _|     ]
  {COLOUR_PALATE["main_text"]} | |_     ]
  {COLOUR_PALATE["light_blue"]} |  _|    ]
  {COLOUR_PALATE["light_blue"]} | |      ]
  {COLOUR_PALATE["light_blue"]} |_|      ]''', ']'),

      # macos :)
      "darwin": make_art(f'''                   ]
      {COLOUR_PALATE["red"]}__ :'__       ]
    {COLOUR_PALATE["orange"]}.'`__`-'__``.    ]
  {COLOUR_PALATE["gold"]}:__________.-'    ]
  {COLOUR_PALATE["main_text"]}:_________:       ]
    {COLOUR_PALATE["magenta_purple"]}:_________`-;    ]
    {COLOUR_PALATE["magenta"]}`.__.-.__.\'      ]''', ']'),

      # pop os :)
      "pop!_os": make_art(f'''                 ]
    {COLOUR_PALATE["light_blue"]}_ __   ._.     ]
  {COLOUR_PALATE["light_blue"]}| '_ \\  | |     ]
  {COLOUR_PALATE["light_blue"]}| |_) | | |     ]
  {COLOUR_PALATE["light_blue"]}| .__/   \\|     ]
  {COLOUR_PALATE["light_blue"]}| |      __     ]
  {COLOUR_PALATE["light_blue"]}|_|      \\/     ]''', ']'),

      # void :)
      "void": make_art(f'''                 ]
    {COLOUR_PALATE["green"]}_ {COLOUR_PALATE["light_green"]}\\\\______     ]
  {COLOUR_PALATE["green"]}| \\  {COLOUR_PALATE["light_green"]}___  \\\\    ]
  {COLOUR_PALATE["green"]}|   {COLOUR_PALATE["light_green"]}/   \\ |     ]
  {COLOUR_PALATE["green"]}|   {COLOUR_PALATE["light_green"]}\\___/ |     ]
  {COLOUR_PALATE["green"]}|  {COLOUR_PALATE["light_green"]}\\______ \\\\   ]
    {COLOUR_PALATE["green"]}-_______\\      ]''', ']'),

      # mageia :)
      "mageia": make_art(f'''             ]
      {COLOUR_PALATE["white_text"]}* .` `   ]
    {COLOUR_PALATE["white_text"]}. . ` .    ]
  {COLOUR_PALATE["white_text"]}|⎻____⎻|    ]
  {COLOUR_PALATE["white_text"]}|        |   ]
  {COLOUR_PALATE["white_text"]}\\      /    ]
    {COLOUR_PALATE["white_text"]}⎻⎻⎻⎻⎻⎻     ]''', ']'),

      # zorin :)
      "zorin os": make_art(f'''                   ]
      {COLOUR_PALATE["light_blue"]},&&&&&&&,      ]
    {COLOUR_PALATE["light_blue"]}/         \\     ]
  {COLOUR_PALATE["light_blue"]}&&&&&&&**  .&&&   ]
    {COLOUR_PALATE["light_blue"]}&&*\'\'   \'***&    ]
    {COLOUR_PALATE["light_blue"]}\\         /     ]
      {COLOUR_PALATE["light_blue"]}\'&&&&&&&\'      ]''', ']'),

      # mint :)
      "linux mint": make_art(f'''               ]
  {COLOUR_PALATE["light_green"]}||            ]
  {COLOUR_PALATE["light_green"]}||            ]
  {COLOUR_PALATE["light_green"]}||/⎻⎻||⎻⎻\\    ]
  {COLOUR_PALATE["light_green"]}|||  ||  |    ]
  {COLOUR_PALATE["light_green"]}|||  ||  |    ]
  {COLOUR_PALATE["light_green"]}\\\\_______/    ]''', ']'),

      # archman :)
      "archman linux": make_art(f'''               ]
        {COLOUR_PALATE["red"]},        ]
      {COLOUR_PALATE["red"]},,,       ]
      {COLOUR_PALATE["red"]},,,,,      ]
    {COLOUR_PALATE["red"]},,,,,,,     ]
    {COLOUR_PALATE["red"]}.,{COLOUR_PALATE["white_text"]}* & *{COLOUR_PALATE["red"]},.    ]
  {COLOUR_PALATE["red"]}., {COLOUR_PALATE["white_text"]} & &  {COLOUR_PALATE["red"]},.   ]''', ']'),

      # android ?
      "android": make_art(f'''                       ]
    {COLOUR_PALATE["light_green"]}&             &     ]
      {COLOUR_PALATE["light_green"]}&           &      ]
      {COLOUR_PALATE["light_green"]}-&&&&&&&&&&&-      ]
    {COLOUR_PALATE["light_green"]}a&&&&&&&&&&&&&&&a    ]
  {COLOUR_PALATE["light_green"]}a&&  &&&&&&&&&  &&a   ]
  {COLOUR_PALATE["light_green"]}&&&&&&&&&&&&&&&&&&&   ]
  {COLOUR_PALATE["light_green"]}&&&&&&&&&&&&&&&&&&&   ]''', ']'),

      # centos:)
      "centos linux": make_art(f'''               ]
  {COLOUR_PALATE["light_green"]}----{COLOUR_PALATE["gold"]}/-\\{COLOUR_PALATE["magenta_purple"]}----   ]
  {COLOUR_PALATE["light_green"]}+\\   {COLOUR_PALATE["gold"]}|{COLOUR_PALATE["magenta_purple"]}   /+   ]
  {COLOUR_PALATE["light_green"]}+ \\  {COLOUR_PALATE["gold"]}|{COLOUR_PALATE["magenta_purple"]}  / +   ]
  {COLOUR_PALATE["light_green"]}<=---{COLOUR_PALATE["white_text"]}*{COLOUR_PALATE["magenta_purple"]}---=>   ]
  {COLOUR_PALATE["normal_text"]}+ /  {COLOUR_PALATE["gold"]}|  \\ +   ]
  {COLOUR_PALATE["normal_text"]}+/__ {COLOUR_PALATE["gold"]}| __\\+   ]''', ']'),

      # endless OS :)
      "endless": make_art(f'''                 ]
              {COLOUR_PALATE["orange"]}_'  ]
    {COLOUR_PALATE["orange"]}.--__  __--.   ]
  {COLOUR_PALATE["orange"]}-   __--__   -  ]
    {COLOUR_PALATE["orange"]}'--__--  --'   ]
      {COLOUR_PALATE["orange"]}_            ]
    {COLOUR_PALATE["orange"]}-             ]''', ']'),

      # OpenBSD :)
      "openbsd": make_art(f'''                  ]
      {COLOUR_PALATE["gold"]}\\\\-`````-/_   ]
  {COLOUR_PALATE["gold"]}_*\\-`       `\\   ]
  {COLOUR_PALATE["gold"]}/^       0 0 \\   ]
  {COLOUR_PALATE["gold"]}\\-\\ <  )  {COLOUR_PALATE["light_red"]}3{COLOUR_PALATE["gold"]}  )   ]
  {COLOUR_PALATE["gold"]}/*\\/         /   ]
    {COLOUR_PALATE["gold"]}//-____*-\\^    ]''', ']'),

      # free bsd :)
      "freebsd": make_art(f'''                  ]
  {COLOUR_PALATE["red"]}/`\\.-^^^^^-./`\\  ]
  {COLOUR_PALATE["red"]}\\  )       (  /  ]
    {COLOUR_PALATE["red"]}|           |   ]
    {COLOUR_PALATE["red"]}|           |   ]
    {COLOUR_PALATE["red"]}*         *    ]
      {COLOUR_PALATE["red"]}`-_____-`     ]''', ']'),

      # tiny core :)
      "tinycore": make_art(f'''
    {COLOUR_PALATE["white_text"]},adPPYba,   
  {COLOUR_PALATE["white_text"]}a8\"     \"8a  ]
  {COLOUR_PALATE["white_text"]}8b      ]     
            {COLOUR_PALATE["white_text"]}d8  
  {COLOUR_PALATE["white_text"]}\"8a,   ,a8\"  
    {COLOUR_PALATE["white_text"]}`\"YbbdP"\'   ]''', ']'),

      # damn small linux :)
      "damn small linux": make_art(f'''          ]
    {COLOUR_PALATE["white_text"]}.~.     ]
    {COLOUR_PALATE["white_text"]}/{COLOUR_PALATE["gold"]}V{COLOUR_PALATE["white_text"]}\\     ]
  {COLOUR_PALATE["white_text"]}// \\\\    ]
  {COLOUR_PALATE["white_text"]}/(   )\\   ]
  {COLOUR_PALATE["gold"]}^`~'^    ]
  {COLOUR_PALATE["light_blue"]}         ]''', ']'),
  }

  # terminal commands (i'd make another file and imported it using a dictionary
  # and functions, but
  # i don't want to make any other files just in case
  try:
      # if xxx == 'xxx' is checking if something is equal to something
      # args is a list of terminal argumemts
      if args == '-c':
          print('''Art By: https://roly.neocities.org/
  Coded By: https://acactusinpain.neocities.org/''')
          
      elif args == '-d':
          print(Art.art(username, hostname, distro, kernel, system_uptime, pacs[0], pacs[1], disk_total, disk_used,
                        ram_total,
                        ram_used, art_list[artName]))
          
      elif args == '-D':
          for key in art_list:
              print(key)
          
      elif args == '-h':
          print('''-c - display the credits
  -d "[distro name]" - display a distro of your choice
  -D - display available distro names
  -h - display this page''')
          
  # if either the distro doesn't exist in the list or too little arguments: do nothing
  except (IndexError, KeyError):
      pass

  try:
      print(Art.art(username, hostname, distro, kernel, system_uptime, pacs[0], pacs[1], disk_total, disk_used, ram_total,
                    ram_used, art_list[distro.lower()]))
  # if the distro doesn't exist use the default linux logo
  except KeyError:
      print(Art.art(username, hostname, distro, kernel, system_uptime, pacs[0], pacs[1], disk_total, disk_used, ram_total,
                    ram_used, art_list["linux"]))