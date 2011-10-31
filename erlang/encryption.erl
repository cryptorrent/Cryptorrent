-module(encryption).
-export([public_encrypt/2,public_decrypt/2,private_encrypt/2,private_decrypt/2]).
-import(crypto).


%% REDO with public_key module

%%
%% rsa_public_encrypt(PlainText, PublicKey, Padding) -> ChipherText
%% rsa_public_decrypt(ChipherText, PublicKey, Padding) -> PlainText
%%
%% Padding = rsa_pkcs1_padding
%% PublicKey = [E, N]
%%   E, N = Mpint
%%   Where E is the public exponent and N is public modulus.
%% The size of the Msg must be less than byte_size(N)-11
%% 
public_encrypt(Message, PublicKey) ->
  crypto:rsa_public_encrypt(Message, PublicKey, rsa_pkcs1_padding)

public_decrypt(Message, PublicKey) ->
  crypto:rsa_public_decrypt(Message, PublicKey, rsa_pkcs1_padding)

%%
%% rsa_private_encrypt(PlainText, PrivateKey, Padding) -> ChipherText
%% rsa_private_decrypt(ChipherText, PrivateKey, Padding) -> PlainText
%%
%% PrivateKey = [E, N, D]
%%    E, N, D = Mpint
%%    Where E is the public exponent, N is public modulus and D is the private exponent.
%%
%% Padding = rsa_pkcs1_padding
%%
%% The size of the Msg must be less than byte_size(N)-11
%%

private_encrypt(Message, PrivateKey) ->
  crypto:rsa_privatec_encrypt(Message, PrivateKey, rsa_pkcs1_padding)

private_decrypt(Message) ->
    crypto:rsa_privatec_decrypt(Message, PrivateKey, rsa_pkcs1_padding)

