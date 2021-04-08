# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 Philipp Temminghoff
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import xbmc
import sys


def main():
    info = sys.listitem.getVideoInfoTag()
    dbid = info.getDbId()
    db_type = info.getMediaType()
    BASE = "RunScript(script.artwork.downloader,"
    if not dbid:
        dbid = sys.listitem.getProperty("dbid")
    if db_type == "movie" or db_type == "tvshow" or db_type == "musicvideo":
        xbmc.executebuiltin("%smediatype=%s,dbid=%s)" % (BASE, db_type, dbid))


if __name__ == '__main__':
    main()

