using UnityEngine;
using System.Collections;

public class _05_CoinRotation : MonoBehaviour {

	//宣告旋轉速度
	public float RotationSpeed;
	// Update is called once per frame
	void Update () {
		//讓物件 Y 軸每秒旋轉
		transform.Rotate (0,RotationSpeed*Time.deltaTime,0);
	}
}
