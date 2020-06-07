using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class LevelMan : MonoBehaviour
{
    public GameObject player;

    public GameObject[] StagePrefabs;

    public GameObject ground;

    private Vector3 direction = new Vector3(0, 0, 1);

    private List<GameObject> stages = new List<GameObject>();

    // Start is called before the first frame update
    void Start()
    {
        //Vector3 pos = this.transform.position + new Vector3(10, 10, -10);
        //Camera.main.transform.position = pos;
        //Camera.main.transform.LookAt(player.transform.position);
        stages.Add(this.gameObject);

        ground.GetComponent<Renderer>().material.color = new Color(0.7f, 0.9f, 0.8f);

        CreateStageAndChangeDirection();
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    void OnCollisionEnter(Collision collision)
    {
        
    }

    int stageIndex = 0;
    public void CreateStageAndChangeDirection()
    {
        //stageIndex = (stageIndex + 1) % 2;
        GameObject prefab = this.StagePrefabs[stageIndex];
        GameObject stage = Instantiate(prefab);
        GameObject last = this.stages.Count == 0 ? this.gameObject : this.stages[this.stages.Count - 1];

        stage.transform.position = last.transform.position + direction * Helper.RandSelectInt(6, 16);
        int scale = Helper.RandSelectInt(2, 4);
        stage.transform.localScale = new Vector3(scale, 1, scale);
        stage.transform.parent = this.transform.parent;

        this.stages.Add(stage);

        Vector3 pos = last.transform.position;
        pos.y = Camera.main.transform.position.y;
        AnimMove.MoveTo(Camera.main.gameObject, 2, pos);

        if (direction==Vector3.forward)
        {
            direction = Vector3.left;
        }
        else
        {
            direction = Vector3.forward;
        }
    }

    public Vector3 GetLastStageDir()
    {
        Vector3 pos1 = this.stages[this.stages.Count - 2].transform.position;
        Vector3 pos2 = this.stages[this.stages.Count - 1].transform.position;
        return (pos2 - pos1).normalized;
    }
}
