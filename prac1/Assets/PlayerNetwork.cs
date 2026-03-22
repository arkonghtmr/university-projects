using UnityEngine;
using Unity.Netcode;
using FixedString = Unity.Collections.FixedString32Bytes;

public class PlayerNetwork : NetworkBehaviour
{
    public NetworkVariable<FixedString> Nickname =
        new NetworkVariable<FixedString>(
            "Player",
            NetworkVariableReadPermission.Everyone,
            NetworkVariableWritePermission.Server
        );

    public NetworkVariable<int> HP =
        new NetworkVariable<int>(
            100,
            NetworkVariableReadPermission.Everyone,
            NetworkVariableWritePermission.Server
        );

    public override void OnNetworkSpawn()
    {
        if (IsOwner)
        {
            string nick = PlayerPrefs.GetString("nickname", "");
            Debug.Log("LOADED NICK: " + nick);
            SubmitNicknameServerRpc(nick);
        }
    }

    [ServerRpc]
    void SubmitNicknameServerRpc(string nick, ServerRpcParams rpcParams = default)
    {
        if (string.IsNullOrWhiteSpace(nick))
        {
            nick = $"Player_{OwnerClientId}";
        }

        Nickname.Value = nick;
    }
}