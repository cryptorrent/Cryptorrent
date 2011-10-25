-module(filemanager).
-export([]).
-import(filelib).     %% for searching and sizing files
-import(file).        %% for opening and managing files



find_file(filename) ->
  