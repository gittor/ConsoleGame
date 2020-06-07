using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class AnimMove : MonoBehaviour
{
    public static void MoveTo(GameObject moveObj, float seconds, Vector3 target)
    {
        AnimMove move = moveObj.AddComponent<AnimMove>();
        move.totalSeconds = seconds;
        move.moveLen = target - moveObj.transform.position;
    }

    private float totalSeconds;
    private float usedSeconds = 0;
    private Vector3 moveLen;

    void Start()
    {
        
    }

    void Update()
    {
        usedSeconds += Time.deltaTime;

        if (usedSeconds>totalSeconds)
        {
            Destroy(this);
            return;
        }

        float ratio = Time.deltaTime / totalSeconds;
        Vector3 movediff = moveLen * ratio;

        this.transform.position += movediff;
    }
}
