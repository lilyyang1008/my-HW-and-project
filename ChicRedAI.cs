using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ChicRedAI : MonoBehaviour
{
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        if(transform.position.y<-2)
        {
            MainAI.Score=MainAI.Score-1;
            MainAI.Life=MainAI.Life-1;
            Destroy(gameObject);
        }
    }
    private void OnCollisionEnter(Collision collision)
    {
        if (collision.gameObject.name == "chick_yellow(Clone)" || collision.gameObject.name == "chick_red(Clone)")
        {
            FixedJoint Fixed_Joint=gameObject.AddComponent<FixedJoint>();
            Fixed_Joint.connectedBody=collision.rigidbody;
        }
    }
}
