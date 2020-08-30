using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public enum TileState
{
    Normal,
    Opened,
    Flagged,
}

public class Tile : MonoBehaviour
{
    public float Width => (this.gameObject.transform as RectTransform).rect.width;
    public float Height => (this.gameObject.transform as RectTransform).rect.height;

    public int Row;
    public int Col;
    public int Number;

    public Image Num;
    public Image Flag;
    public GameObject Mouse;
    public GameObject DebugNode = null;
    public Sprite[] NumImages = new Sprite[8];
    public Sprite[] TubeImages = new Sprite[2];

    private bool ismine;
    public bool IsMine
    {
        get
        {
            return ismine;
        }
        set
        {
            ismine = value;
            if (DebugNode)
            {
                DebugNode.SetActive(value);
            }
        }
    }

    public TileState State = TileState.Normal;

    public void Init()
    {
        TrySetState(TileState.Normal);
        Mouse.SetActive(false);
    }

    public bool Scaled
    {
        get
        {
            return gameObject.transform.localScale.y != 1;
        }
        set
        {
            Vector3 scale = gameObject.transform.localScale;
            if (value)
            {
                scale.y = 0.7f;
            }
            else
            {
                scale.y = 1;
            }
            gameObject.transform.localScale = scale;
        }
    }

    public bool HitTest(Vector3 worldPos)
    {
        Vector3 local = gameObject.transform.InverseTransformPoint(worldPos);
        local.z = 0;

        if (local.magnitude<55)
        {
            return true;
        }
        return false;
    }

    public void TrySetState(TileState state)
    {
        if (state == TileState.Normal)
        {
            State = TileState.Normal;
            Num.gameObject.SetActive(false);
            Flag.gameObject.SetActive(false);
            gameObject.GetComponent<Image>().sprite = TubeImages[0];
        }
        else if (state == TileState.Opened)
        {
            if (State == TileState.Normal)
            {
                if (Number == 0)
                {
                    Num.gameObject.SetActive(false);
                }
                else
                {
                    Num.gameObject.SetActive(true);
                    Num.gameObject.GetComponent<Image>().sprite = NumImages[Number - 1];
                }
                gameObject.GetComponent<Image>().sprite = TubeImages[1];

                State = TileState.Opened;
            }
        }
        else if (state == TileState.Flagged)
        {
            if (State == TileState.Normal)
            {
                Flag.gameObject.SetActive(true);
                State = TileState.Flagged;
            }
        }
    }

    public void SetFailed(bool answer)
    {
        if (!IsMine)
            return;

        Mouse.SetActive(true);
        Mouse.GetComponent<Animator>().SetBool("MouseAnim", true);
        

        if (answer)
        {
            Mouse.GetComponent<Image>().color = Color.red;
        }
    }

    public void SetSucceed()
    {
        if (!IsMine)
            return;

        Mouse.SetActive(true);
        Mouse.GetComponent<Animator>().SetBool("MouseAnim", true);
    }
}
