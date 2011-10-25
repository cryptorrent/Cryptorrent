-module(gossip).
-export([]).
-import(encryption).
-import(filemanager).
-import(timer).       %% for periodic functions
-import(ets).         %% for info storage





%%
%% apply_interval(Time, Module, Function, Arguments) ->
%%                  {ok, TRef} | {error, Reason}
%%
%%  Time is in ms


initiate() ->
  apply_interval(2, gossip, initiate_gossip, []).


initiate_gossip() ->
  