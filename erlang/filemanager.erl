-module(filemanager).
-export([]).
-import(filelib).
-import(file).
-import(dict).

%%
%% @param Filemap = dictionary mapping Xids to a list describing
%%                  the bounds of received file chunks.
%%
%% Supports the messages:
%%  file_check, Req, Filename -> {exists, Filesize} or {dne}
%%  
%%  r_chunk, Req, Filename, Start, End -> {ok, Chunk} or {error, Msg}
%%
%%  w_chunk, Req, Filename, Start, End -> {ok} or {error, Msg}
%%
file_manager(Filemap) ->
    receive
	{file_check, Req, Filename} ->
	    case filelib:is_file(Filename) of
		true ->
		    Req ! filelib:file_size(Filename);
		false ->
		    Req ! {dne}
	    end,
	    file_manager(Filemap);
	{r_chunk, Req, Filename, Start, End} ->
	    Req ! read_chunk(Filename, Start, End),
	    file_manager(Filemap);
	{w_chunk, Req, Xid, Filename, Start, End}->
	    Req ! receive_chunk(Filemap, Xid, Filename, Start, End)
    end.

%%
%% Reads a file and returns the file size (for a success) or
%% "dne" for a failure (does not exist).
%%
read_chunk(Filename, Start, End) ->
    case file:open(Filename, [read, raw, binary]) of
	{ok, F} ->
	    Output = file:pread(F, Start, End),
	    file:close(F);
	{error, Reason} ->
	    Output = {error, Reason}
    end,
    Output.

%%
%% Takes in file chunks and writes out dummy parts of
%% the file in the places in which it is missing chunk.
%% Also writes out a local/temporary descriptor of the chunk
%% that have been collected, for error recovery.
%%
receive_chunk(Filemap, Xid, Filename, Start, End) ->
    pass,
    file_manager(Filemap).

write_chunk(Filename, Bytes) ->
  case file:open(Fname, [write, append, raw, binary]) of
    {ok} ->
      Output = file:write(F, Bytes);
    {error, Reason} ->
      Output = {error, Reason}
  end,
  Output.
