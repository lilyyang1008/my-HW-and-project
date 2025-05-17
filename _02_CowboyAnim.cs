using UnityEngine;
using System.Collections;

public class _02_CowboyAnim : MonoBehaviour {

	Animator AnimatorCowboy;   //宣告角色動畫
	public  bool BoolRun, BoolJump, BoolJumpLeft, BoolJumpRight, BoolOver;
	//宣告跑,跳,左跳,右跳,闖關失敗的動畫開關
	public  float RunAnimSpeed, JumpLeftAnimSpeed, JumpRightAnimSpeed;
	//宣告跑,左跳,又跳的動畫播放速度
	// Use this for initialization
	void Start () {
		AnimatorCowboy = GetComponent<Animator> ();
	}
	
	// Update is called once per frame
	void Update () {
		//動畫開關的宣告對應自身動畫中參數設定
		AnimatorCowboy.SetBool ("BoolRun",BoolRun);
		AnimatorCowboy.SetBool ("BoolJump",BoolJump);
		AnimatorCowboy.SetBool ("BoolJumpLeft",BoolJumpLeft);
		AnimatorCowboy.SetBool ("BoolJumpRight",BoolJumpRight);
		AnimatorCowboy.SetBool ("BoolOver",BoolOver);
		//動畫播放速度的宣告對應自身動畫中參數設定
		AnimatorCowboy.SetFloat ("RunAnimSpeed",RunAnimSpeed);
		AnimatorCowboy.SetFloat ("JumpLeftAnimSpeed",JumpLeftAnimSpeed);
		AnimatorCowboy.SetFloat ("JumpRightAnimSpeed",JumpRightAnimSpeed);
	}
	void JumpLREnd(){
		//關閉左跳動畫
		BoolJumpLeft = false;
		//關閉右跳動畫
		BoolJumpRight = false;
	}
}
