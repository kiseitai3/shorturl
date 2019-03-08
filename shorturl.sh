#!/bin/bash
#Shorturl is pythonscript module for tinyfying urls
#    Copyright (C) 2019  Luis Miguel Santos
#    email: luismigue1234@hotmail.com

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
 #   the Free Software Foundation, either version 3 of the License, or
 #   (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
 #   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 #   GNU General Public License for more details.

 #   You should have received a copy of the GNU General Public License
 #   along with this program.  If not, see <https://www.gnu.org/licenses/>.
coproc netcat localhost 5555

while read -r cmd; do
  case "$cmd" in
    i) echo "https://github.com/kiseitai2/Engine_Eureka/blob/master/Dependencies/Python27/include/bufferobject.h" ;;
    d) date ;;
    q) kill "$COPROC_PID"
       exit ;;
    *) echo "What?" ;;
  esac
done <&${COPROC[0]} >&${COPROC[1]}
