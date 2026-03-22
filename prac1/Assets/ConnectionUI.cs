using UnityEngine;
using Unity.Netcode;

public class ConnectionUI : MonoBehaviour
{
    public NicknameUI nicknameUI;

    public void StartHost()
    {
        nicknameUI.SaveNickname(); // ВАЖНО!
        NetworkManager.Singleton.StartHost();
    }

    public void StartClient()
    {
        nicknameUI.SaveNickname(); // ВАЖНО!
        NetworkManager.Singleton.StartClient();
    }
}