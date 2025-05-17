using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CameraRotate : MonoBehaviour
{
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }
    public void LeftButtonDown()
    {
        transform.Rotate(0,2,0, Space.World);
    }
    public void RightButtonDown() 
    { 
        transform.Rotate(0,-2,0, Space.World);
    }
}
