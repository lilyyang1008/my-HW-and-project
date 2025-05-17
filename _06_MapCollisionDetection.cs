using UnityEngine;
using System.Collections;

public class _06_MapCollisionDetection : MonoBehaviour {

	//進入觸發器偵測
	void OnTriggerEnter(Collider CollisionDetection){
		//如果進入觸發器的物件標籤名稱為 Map
		if (CollisionDetection.tag == "Map") {
			//改變進入觸發器物件標籤為 RnuMap
			CollisionDetection.tag = "RunMap";
		}
	}
	//離開觸發器偵測
	void OnTriggerExit(Collider CollisionDetection){
		//如果離開觸發器的物件標籤名稱為 RunMap
		if (CollisionDetection.tag == "RunMap") {
			//銷毀離開觸發器標籤為 RunMap 的物件
			Destroy(CollisionDetection.gameObject);
		}
	}
}

