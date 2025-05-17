using UnityEngine;
using System.Collections;
//增加 UI 運用
using UnityEngine.UI;
using UnityEngine.SceneManagement;

public class _01_GameControl : MonoBehaviour {
	//宣告判斷遊戲是否結束
	public static bool GameOverBool;
	//宣告金幣數量
	public static int CoinNumber;
	//宣告金幣數量顯示文字介面
	public GameObject CoinNumberText;
	//宣告遊戲場景地圖遊戲物件陣列
	public GameObject[] Map;
	//宣告地圖連續產生的間隔距離
	int MapDistance;
	//宣告牛仔角色遊戲物件，將取得牛仔角色的Z軸作為移動距離
	public GameObject Cowboy;
	//宣告主介面的牛仔跑步距離文字顯示物件
	public GameObject RunDistanceText;
	//宣告訊息介面遮罩物件，訊息介面暫停/開始按鈕物件
	public GameObject MessageMaskUI,PlayStopButton;
	//宣告訊息介面暫停/開始按鈕物件的2張切換圖片
	public Sprite UI_02, UI_03;
	//宣告結算得分
	int Score;
	//5-3宣告閱關失敗介面的遮罩物件,金幣數量文字物件,跑步距離文字物件,分數結算文字物件
	public GameObject EndMaskUI, EndCoinNunberText, EndRunDistanceText, EndScoreText;
	// Use this for initialization
	void Start () {
		//預設遊戲不在結束狀態
		GameOverBool = false;
		//初始金幣數量為 0
		CoinNumber = 0;
		//地圖產生間隔距離初始化為 0
		MapDistance = 0;
		//預設訊息介面為隱藏狀態
		MessageMaskUI.SetActive (false);
		//預設闖關失敗介面為隱藏狀態 
		EndMaskUI.SetActive (false);

	}
	
	// Update is called once per frame
	void Update () {
		//前往執行 UI 顯示
		UguiShow ();
		//前往執行連續地圖產生判斷
		ProduceMap ();
		//如果遊戲結束
		if (GameOverBool == true) {
			//在除錯視窗顯示 GameOver
			print("GameOver");
			//顯示闖關失敗介面
			EndMaskUI.SetActive(true);
			if(Score > PlayerPrefs.GetInt("Score")){
			//將當前的分數儲存在 Score 儲存欄中
				PlayerPrefs.SetInt("Score",Score);
			}
		}
	}
	//UI 顯示
	void UguiShow(){
	//介面顯示當前獲得的金幣數量
		CoinNumberText.GetComponent<Text> ().text = "" + CoinNumber;
		//介面顯示當前跑步距離，以無條件捨去法顯示牛仔角色移動Z軸的數值 
		RunDistanceText.GetComponent<Text> ().text = "" + Mathf.FloorToInt (Cowboy.transform.position.z);
		//闖關失敗介面顯示獲得金幣數量
		EndCoinNunberText.GetComponent<Text> ().text = "" + CoinNumber; 
		//闖關失敗介面顯示跑步距離，以無條件捨去的方式顯示牛仔角色移動Z軸的數值
		EndRunDistanceText.GetComponent<Text> ().text ="" + Mathf.FloorToInt (Cowboy.transform.position.z);
		//得分計算方式為，擭得金幣數量*10加上無條件捨去的牛仔角色Z軸數值
		Score = (CoinNumber * 10)+(Mathf.FloorToInt (Cowboy.transform.position.z));
		//閲關失敗介面顯示結算後的得分數
		EndScoreText.GetComponent<Text> ().text = "" + Score;
	}
	//連續地圖產生判斷
	void ProduceMap (){
		//宣告尋找標籤為 Map 的遊戲物件
		GameObject FindMap = GameObject.FindGameObjectWithTag ("Map");
		//如果為標籤 Map 的遊戲物件不存在時
		if (FindMap == null) {
			//地圖連續產生的間隔距離 +16
			MapDistance +=16;
			//隨機陣列中的地圖陣列順序
			int RandomMap = Random.Range(0, Map.Length);
			//產生陣列中亂數 RandomMap 的順序地圖, 間隔距離, 旋轉值歸零
			Instantiate(Map[RandomMap], new Vector3(0,0,MapDistance), Quaternion.identity);
		}
       
    }
	public void PlayStop(){
		//如果主介面的暫停/開始按鈕圖片名稱為UI_02，暫停圖片
		if (PlayStopButton.GetComponent<Image> ().sprite.name == "UI_02") {
			//將圆片更換為UI_03，開始圖片
			PlayStopButton.GetComponent<Image> ().sprite = UI_03; 
			//顯示訊息介面
			MessageMaskUI.SetActive (true);
			//增加開始倒數時間3秒
			_09_CowboyControlMobile.StartReciprocalTime = 3;                    //_08_CowboyControlMouse.StartReciprocalTime = 3;
			//遊戲時間運行速度為0，暫停遊戲
			Time.timeScale = 0;
		} else {  //如果主介面的暫停/開始按鈕圖片名稱為UI_03，開始圖片 
			//將圖片更換為UI_02，暫停圖片
			PlayStopButton.GetComponent<Image> ().sprite = UI_02;
			//隱藏訊息介面
			MessageMaskUI.SetActive (false);
			//遊戲時間運行速度為1，正常運行 
			Time.timeScale = 1;
		}
	}
	//返回主選單按鈕
	public void MenuButton(){
        //場景轉跳至主選單
        SceneManager.LoadScene("CowboyCool_Menu");
	}
	//訊息介面的繼續遊戲按鈕
	public void MessagePlayButton() {
		//隱藏訊息介面
		MessageMaskUI.SetActive (false);
		//主介面的暫停/開始按鈕圖片更換為UI_02，暫停圖片
		PlayStopButton.GetComponent<Image> ().sprite = UI_02;
		//遊戲時間運行速度為1，正常運行
		Time.timeScale = 1;
	}
	//再玩一次按鈕
	public void EndAgainButton(){
        //重新載入遊戲主場景，可以重新運行所有腳本 
        SceneManager.LoadScene("CowboyCool_MainScene");
	}
}
