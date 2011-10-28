-module(gossip).
-export([]).
-import(encryption).
-import(filemanager).
-import(timer).       %% for periodic functions
-import(dict).         %% for info storage
-import(gen_udp).



%% Gossip Manager %%

initialize_gossip_manager() ->
    GossipManager = spawn(gossip_manager, [dict:new(), dict:new()]),
    spawn(gossip_server, [GossipManager]).
    apply_interval(10000, gossip, initiate_gossip, [GossipManager]).

gossip_manager(Hosts, FileRequests) ->
    receive
	{process, Gossip} -> 
	    process_gossip(Gossip, Hosts, FileRequests).
	{generate, Req} ->
	    Req ! generate_gossip_set(Hosts, FileRequests),
	    gossip_manager(Hosts, FileRequests);
    end.

generate_gossip_set(Hosts, FileRequsts) ->
    pass,
    {generated, Gossip}.

process_gossip(Gossip, Hosts, FileRequsts) ->
    pass,
    gossip_manager(Hosts, FileRequsts).



%% Gossip Server %%

gossip_server(GossipManager) ->
    {ok, Socket} = gen_udp:open(8099, [binary]),
    loop(Socket, GossipManager).

loop(Socket, GossipManager) ->
    receive
        {udp, Socket, Host, Port, Bin} = Msg ->
	    spawn(udp_message_handler, [GossipManager, Socket, Host, Port, Bin]),
            loop(Socket)
    end.

udp_message_handler(GossipManager, Socket, Host, Port, Bin) ->
    InGossip = binary_to_term(Bin),
    OutGossip = generate_gossip(GossipManager),
    gen_udp:send(Socket, Host, Port, term_to_binary(OutGossip)),
    process_gossip(GossipManager).

%% Gossip Client %%

initiate_gossip(GossipManager) ->
    Host = choose_host(),
    Gossip = generate_gossip(),
    InGossip = gossip(Gossip, Host),
    GossipManager ! {process, Gossip}.

gossip(Gossip, Host) ->
    {ok, Socket} = gen_udp:open(0, [binary]),
    ok = gen_udp:send(Socket, Host, 8099,
                      term_to_binary(Gossip)),
    InGossip = receive
                {udp, Socket, _, _, Bin} = Msg ->
                    binary_to_term(Bin)
            after 2000 ->
                    0
            end,
    gen_udp:close(Socket),
    InGossip.

generate_gossip(GossipManager) ->
    GossipManager ! {generate, self()},
    receive
	{generated, Gossip} ->
	    Gossip
    end.
