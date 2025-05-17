using UnityEngine;
using System.Collections;
//增加 UI 運用
using UnityEngine.UI;

public class _08_CowboyControlMouse : MonoBehaviour {
	
	bool  Challenge;     //宣告闖關挑戰判斷
	public  float  CowboyRunSpeed;    //宣告角色移動速度
	bool  OnFloor;      //宣告角色是否站在地板上的判斷
	public  float  JumpHigh;   //宣告角色跳躍時的向上作用力
	int   CowboyRunway;  //宣告角色在跑到的位置  
	public  float  ChangingRunwaySpeed;   //宣告角色切換跑道的速度
	public  GameObject  JumpSound, RunSmoke;   //宣告跳躍時的音效遊戲物件, 跑步時的煙霧效果
	//宣告獲得金幣特效, 獲得金幣音效, 撞到牆音效
	public GameObject CoinsEffects, GetCoinSound, HitSound;  
	//宣告開始闖關的倒數時間
	public static float StartReciprocalTime;
	//宣告開始闖關的倒數文字物件
	public GameObject StartReciprocalTimeText;
	//宣告滑鼠按下 2 維座標、滑鼠離開 2 維座標
	Vector2 MouseDownPos, MouseUpPos;
	//宣告滑鼠按下移動後離開的垂直距離和橫向距離
	float HorizontalDistance, VerticalDistance;

	// Use this for initialization
	void Start () {
		Challenge = true;   //預設為可以闖關挑戰
		transform.position = new Vector3 (0,0.25F,0);  //初始化角色預設位置
		CowboyRunway = 0;   //初始化角色在跑道中間
		StartReciprocalTime = 0;  //預設闖關開始倒數時間為3
		//預設煙霧特效的發射元件停用
		RunSmoke.GetComponent<ParticleSystem> ().enableEmission = false;
	}
	
	// Update is called once per frame
	void Update () {
		//如果闖關挑戰為真
		if (Challenge == true) {
			//如果閬關開始倒數時間大於0
			if(StartReciprocalTime >0){
				StartReciprocalTime -= Time.deltaTime; //開始倒數
				//倒數顯示文字物件以無條件進位的方式顯示倒數時間
				StartReciprocalTimeText.GetComponent<Text>().text = ""+Mathf.CeilToInt(StartReciprocalTime);
				//煙霧特效的發射元件停用
				RunSmoke.GetComponent<ParticleSystem>().enableEmission = false;
				//關閉跑步動畫
				GetComponent<_02_CowboyAnim> ().BoolRun = false;
			}else {
				//倒數顯示文字物件不顯示任何文字
				StartReciprocalTimeText.GetComponent<Text>().text = "";
				//前往執行闖關挑戰開始
				ChallengeStart();
			}
		}
	}
	
	void ChallengeStart(){
			//角色往前移動，增加Z軸座標
			transform.Translate (0, 0, CowboyRunSpeed * Time.deltaTime);
			//角色開啟跑步動作
			GetComponent<_02_CowboyAnim> ().BoolRun = true;
		    //前往滑鼠座標紀錄和事件衍生
			ControlMouse ();
			//如果角色不在對應的跑道上時
			if (transform.position.x != CowboyRunway) {
				//前往執行移動角色所在位置
				CheckCowboyPosX ();

			//如果角色站在地板上
			if (OnFloor == true) {
				//煙霧特效發射元件啟用
				RunSmoke.GetComponent<ParticleSystem> ().enableEmission = true;
				//如果角色不在地板上
			} else {
				//煙霧特效發射元件停用
				RunSmoke.GetComponent<ParticleSystem> ().enableEmission = false;
			}
			//如果沒有按住鍵盤W鍵時
		} else {
			//角色關閉跑步動作
			GetComponent<_02_CowboyAnim>().BoolRun = false;
			//煙霧特效發射元件停用
			RunSmoke.GetComponent<ParticleSystem> ().enableEmission = false;
		}
	}
	//滑鼠座標紀錄和事件衍生
	void ControlMouse(){
		//5-5如果當滑鼠按下時
		if (Input.GetMouseButtonDown (0)) {
			//紀錄滑鼠按下的座標
			MouseDownPos = Input.mousePosition;
		}
		//如果滑鼠離開時
		if (Input.GetMouseButtonUp (0)) {
			//紀錄滑鼠離開座標
			MouseUpPos = Input.mousePosition;
			//前往執行滑鼠按下和離開之間的移動距離判斷方向選擇 
			DirectionChoose();
		}
	}
	//滑鼠按下和離開之間的移動距離判斷方向選擇
	void DirectionChoose(){
		//垂直距離為滑鼠離開時的座標Y-滑鼠按下時的座標Y
		HorizontalDistance = MouseUpPos.y - MouseDownPos.y;
		//橫向距離為滑鼠離開時的座標X-滑鼠按下時的座標X
		VerticalDistance = MouseUpPos.x - MouseDownPos.x;
		//如果垂直距離大於橫向距離，取正數做距離長度判斷
		if (Mathf.Abs (HorizontalDistance) > Mathf.Abs (VerticalDistance))
		{
			//前往執行往上跳
			JumpMove ();
		}else{    //如果橫向距離大於垂直距離
			//前往執行左右移動
			LeftRight();
		}
	}
	//往上跳
	void JumpMove(){
		//垂直距離值大於0，代表往上滑動，並且角色站在地板上
		if (HorizontalDistance >0 && OnFloor == true) {
			//角色開啟跳躍動作
			GetComponent<_02_CowboyAnim>().BoolJump = true;
			//往上跳，Y軸增加作用力
			GetComponent<Rigidbody>().AddForce(0,JumpHigh,0);
			//跳躍時角色不在地板上
			OnFloor = false;
			//產生跳躍時的音效
			Instantiate(JumpSound,transform.position, Quaternion.identity);
		}
	}
	//左右移動
	void LeftRight(){
		//如果橫向距離值小於0，代表從右往左滑動，並且角色在跑道1或跑道0的位置
		if (VerticalDistance < 0 && CowboyRunway > -1) {
			//角色開啟向左跳躍的動作
			GetComponent<_02_CowboyAnim>().BoolJumpLeft = true;
			//角色向左更換跑道
			CowboyRunway -=1;
			//產生跳躍時的音效
			Instantiate(JumpSound,transform.position, Quaternion.identity);
		}
		
		//如果按下鍵盤D鍵，並且角色在跑道-1或跑道0的位置
		if (VerticalDistance > 0 && CowboyRunway < 1) {
			//角色開啟向右跳躍的動作
			GetComponent<_02_CowboyAnim>().BoolJumpRight = true;
			//角色向右更換跑道
			CowboyRunway +=1;
			//產生跳躍時的音效
			Instantiate(JumpSound,transform.position, Quaternion.identity);
		}
	}
	//移動角色所在位置
	void CheckCowboyPosX(){
		//宣告角色左右移動的線性變化數值，當前角色X座標值，移動到跑道數值，以每秒的移動速度
		float ChangingRunway = Mathf.Lerp (transform.position.x, CowboyRunway, ChangingRunwaySpeed * Time.deltaTime);
		//角色位置，左右移動的線性變化，自身Y軸，自身Z軸
		transform.position = new Vector3 (ChangingRunway, transform.position.y, transform.position.z);
	}
	//當進人角色碰撞器
	void OnCollisionEnter(Collision CowboyCollision){
		//如果角色碰撞器碰到的物件標籤為Floor地扳時
		if (CowboyCollision.collider.tag == "Floor") {
			//關閉角色跳躍動作
			GetComponent<_02_CowboyAnim>().BoolJump = false;
			//角色站在地板上
			OnFloor = true;
		}
		if (CowboyCollision.collider.tag == "Wall") {
			// 開啟角色闖關失敗動作
			GetComponent<_02_CowboyAnim>().BoolOver =true;
			// 闖關挑戰結束
			Challenge = false;
			//遊戲結束
			_01_GameControl.GameOverBool = true;
			//產生撞牆音效
			Instantiate(HitSound,transform.position,Quaternion.identity);
			//煙霧特效的發射元件停用
			RunSmoke.GetComponent<ParticleSystem>().enableEmission = false;
		}
		// 如果角色碰撞器碰到的物件標籤為 Coin 金幣時
		if (CowboyCollision.collider.tag == "Coin") {
			//金幣數量加1
			_01_GameControl.CoinNumber +=1;
			//刪除金幣標籤物件
			Destroy(CowboyCollision.gameObject);
			//產生獲得金幣特效
			Instantiate(GetCoinSound, transform.position, Quaternion.identity);
			//產生獲得金幣特效, 在角色前方 2 公尺處, 上方 1 公尺處
			Instantiate(CoinsEffects, transform.position + new Vector3(0F, 1F, 2F), Quaternion.identity);
		}
	}
}
