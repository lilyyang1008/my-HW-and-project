using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.SceneManagement;

public class MainAI : MonoBehaviour
{
    // Start is called before the first frame update
    public GameObject Chick_Yellow;
    public GameObject Chick_Red;
    public GameObject Chick;
    public GameObject MainCamera;
    private int Amount;
    public static bool IsPress;
    public Image Red_Image;
    public Image Yellow_Image;
    public static int Score;
    public Text ScoreString;
    static bool Shot;
    public static int Life;
    public Text LifeString;
    private float timer;
    public Button ReturnButtom;

    void Start()
    {
        IsPress = false;
        Score = 0;
        Shot = true;
        Life = 10;
        timer = 0;
        ReturnButtom.gameObject.SetActive(false);
    }

    // Update is called once per frame
    void Update()
    {
        if (Input.GetMouseButtonDown(0)&&!IsPress&&Shot)
        {
            Vector3 ShortPos=new Vector3(MainCamera.transform.position.x,
                MainCamera.transform.position.y-0.5f,
                MainCamera.transform.position.z);
            Score++;
            Amount++;
            if (Amount % 5 != 0)
            {
                Chick = Instantiate(Chick_Yellow, ShortPos, Quaternion.Euler(270, 180, 0));
            }
            else
            {
                Chick = Instantiate(Chick_Red, ShortPos, Quaternion.Euler(270, 180, 0));
            }
            if (Amount % 5 == 4)
            {
                Yellow_Image.enabled = false;
                Red_Image.enabled = true;
            }
            else
            {
                Yellow_Image.enabled = true;
                Red_Image.enabled = false;
            }
            Ray MouseRay=Camera.main.ScreenPointToRay(Input.mousePosition);
            Chick.GetComponent<Rigidbody>().AddForce(MouseRay.direction.x * (Input.mousePosition.y / Screen.height * 1200),
                150, MouseRay.direction.z * (Input.mousePosition.y / Screen.height * 1200));
            Chick.GetComponent<Rigidbody>().AddRelativeTorque(-8, 0, 0);
        }
        if (Life < 1)
        {
            Shot=false;
            timer=timer+Time.deltaTime;
            if (timer > 4)
            {
                ReturnButtom.gameObject.SetActive(true);
                Red_Image.enabled = false;
                Yellow_Image.enabled = false;
            }
        }
        ScoreString.text=Score.ToString();
        LifeString.text=Life.ToString();
    }
    public void PlayAgain()
    {
        SceneManager.LoadScene(0);
    }
}
