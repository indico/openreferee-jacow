%
%   Fontmap.GS $Version 1.0 2014.06.13$
%   Copyright (C) 2013-2014 GSI Helmholtzzentrum für Schwerionenforschung GmbH 
%   <http://www.gsi.de> by Raphael Mueller
%
%   This file is free software; you can redistribute it and/or modify
%   it under the terms of the GNU General Public License as published by
%   the Free Software Foundation; either version 2 of the License, or
%   (at your option) any later version.
%
%   This file is distributed in the hope that it will be useful,
%   but WITHOUT ANY WARRANTY; without even the implied warranty of
%   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
%   GNU General Public License for more details.
%
%   You should have received a copy of the GNU General Public License
%   along with this program; if not, write to the Free Software
%   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
%   You can also get a copy of the license through the web at
%   <http://www.gnu.org/licenses/gpl.html>
%

%
% First we include the original fontmap file
%
% Linux example: (/usr/share/ghostscript/8.70/Resource/Init/Fontmap.GS)	.runlibfile
% Windows example: (C:\Program Files\gs\gs8.70\Resource\Init\Fontmap.GS)	.runlibfile
%
% In newer GhostScript versions this might be included into the executable, so
% if you can not find the file you have to download it:
% http://git.ghostscript.com/?p=ghostpdl.git;a=tree;f=gs/Resource/Init
%

(<CONFIGURE YOUR Fontmap.GS PATH here>)	.runlibfile

% Now we define additional mappings that are missing in the original

% Name in PDF                           Font to map it to
% You can use /<name> or (<name>)       If you use /<fontname> its the GS font alias,
% if the name has spaces                if you use (<filename>) you map the font name to a fontfile 
% you must use brackets.

(Times New Roman,Italic)		/Times-Italic			;
(Times New Roman,BoldItalic)		/Times-BoldItalic		;

/TimesNewRomanPSMT                      /Times-Roman                    ;
/TimesNewRomanPS-BoldMT                 /Times-Bold                     ;
/TimesNewRomanPS-ItalicMT               /Times-Italic                   ;
/TimesNewRomanPS-BoldItalicMT           /Times-BoldItalic               ;

