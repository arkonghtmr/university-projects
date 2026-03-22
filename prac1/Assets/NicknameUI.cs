using UnityEngine;
using TMPro;
using UnityEngine.UI;

public class NicknameUI : MonoBehaviour
{
    public TMP_InputField input;

    public void SaveNickname()
    {
        InputField inputField = gameObject.GetComponent<InputField>();
        string nick = inputField.text;

        Debug.Log("BUTTON PRESSED, nick = " + nick);

        PlayerPrefs.SetString("nickname", nick);
    }
}