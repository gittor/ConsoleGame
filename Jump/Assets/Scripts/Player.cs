using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Player : MonoBehaviour
{
    public GameObject head;
    public GameObject bottom;

    public LevelMan levelMan;

    private float touchingTime;

    private int touchState = 0;

    void Start()
    {

    }

    // Update is called once per frame
    void Update()
    {
        if(Input.GetMouseButtonDown(0))
        {
            this.OnMouseButtonDown();
        }
        else if(Input.GetMouseButton(0))
        {
            this.OnMouseButtonTouch();
        }
        else if(Input.GetMouseButtonUp(0))
        {
            this.OnMouseButtonUp();
        }
    }

    void OnMouseButtonDown()
    {
        //if (touchState != -1)
        //    return;

        touchingTime = 0;
        touchState = 1;
    }

    void OnMouseButtonTouch()
    {
        if (touchState != 1)
            return;

        touchingTime += Time.deltaTime;
        if(touchingTime>1)
        {
            touchingTime = 1;
        }

        float scaleY = 1 - touchingTime * 0.8f;
        //bottom.transform.localScale = new Vector3(1, scaleY, 1);
    }

    void OnMouseButtonUp()
    {
        if (touchState != 1)
            return;
        touchState = 2;

        touchingTime = 0;

        bottom.transform.localScale = new Vector3(1, 1, 1);

        Vector3 force = this.levelMan.GetLastStageDir() * 7.5f;
        force.y = 10;
        Rigidbody rigid = GetComponent<Rigidbody>();
        rigid.AddForce(force, ForceMode.Impulse);

        levelMan.CreateStageAndChangeDirection();
    }

    void OnCollisionEnter(Collision collision)
    {
        //startTouched = false;
    }
}
