using UnityEngine;
using System.Collections;
//增加UI運用 
using UnityEngine.UI;

public class _07_MenuControl : MonoBehaviour {

	//宣告最高得分顯示文字物件 
	public GameObject MenuScoreText;

	// Use this for initialization
	void Start () {
		//存檔初始化判斷，如果名稱為Score的存檔內容不存在時
		if (PlayerPrefs.HasKey ("Score") == false) {
			//在Score存擋空間存入0的數字
			PlayerPrefs.SetInt("Score",0);
		}
	
	}
	// Update is called once per frame
	void Update () {
		MenuScoreText.GetComponent<Text>().text = "" + PlayerPrefs.GetInt("Score");

	}
	//開始遊戲按鈕事件
	public void MenuStartButtom() {
		//場景轉換到CowboyCool_MainScene遊戲場景
		Application.LoadLevel ("CowboyCool_MainScene");
	}
	//離開遊戲按鈕事件
	public void MenuExitButton() {
		//離開遊戲
		Application.Quit ();
	}
}
