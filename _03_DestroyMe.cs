using UnityEngine;
using System.Collections;

public class _03_DestroyMe : MonoBehaviour {

	public  float DestroyTime;
	// Update is called once per frame
	void Update () {
		//幾秒後銷毀物件
		Destroy (gameObject, DestroyTime);
	}
}
