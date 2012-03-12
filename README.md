# trelloburndown - Burndown charts for projects in Trello

Trello (http://www.trello.com) is a nice tool for managing lists of things. Those things could be software development tasks, and the lists could be the items that are done and to be done for a sprint. This tool will watch your lists, record some data, and create a pretty graph of your progress.

## Requirements

- An account on trello.com
- cherrypy (http://www.cherrypy.org/)
- requests (python-requests.org)
- sqlalchemy (http://www.sqlalchemy.org/)

## Usage

Fill out the missing values in settings.py (BOARD_ID, API_KEY, USER_TOKEN). http://www.trello.org/help.html can assist with generating the necessary API keys.

Run fetcher.py once a day manually, or use the -d option along with the -f or -t options to have it run continuously.

cherrypy.org has more information about deploying cherrypy apps, but in the simplest case, just run "python server.py" and connect to http://localhost:8080. Create a sprint, view it to edit the dates, and a graph should be created if there is any data to use.

By default, effort estimates from Trello are extracted by looking for "(<number>)" in the task title. get_totals in fetcher.py can be modified to look elsewhere if necessary. The total effort for the sprint is currently just derived from the remaining effort on the first day of the sprint. The names of the lists that constitute remaining effort vs. completed effort can be modified in settings.py.

## License

Copyright (c) 2012, Tony Angerilli
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met: 

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer. 
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution. 

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.