# applications

A set of programs for various purposes written in Java/Python

## battery-guardian.py

Check battery level and notify if it is too low or too high

It is recommended to add the script to cron (below snippet was checked on Ubuntu 18.04):
```
$ (crontab -l; echo "* * * * *  XDG_RUNTIME_DIR=/run/user/$(id -u) {FULL_PATH}/battery-guardian.py") | crontab  
```

Type `$ ./battery-guardian.py -h` to display full help.

## now.py

Print current date and/or time related value for given argument.

```
$ now.py -D
  2019-02-03T16:06:19
```

Type `$ ./now.py -h` to display full help.

## symlinker.py

Create absolute symbolic link to a file.

Difference between `ln -s` and `symlinker.py`:
```
$ ln -s ./foo bar; ls -og | grep bar
  lrwxrwxrwx 1      5 Feb  3 15:44 bar -> ./foo
$ symlinker.py ./foo bar; ls -og | grep bar
  lrwxrwxrwx 1      8 Feb  3 15:45 bar -> /tmp/foo
```

Type `$ ./symlinker.py -h` to display full help.

## tabber.py

Launch terminal with multiple tabs.

Type `$ ./tabber.py -h` to display full help and see `tabber.conf` for sample configuration.
