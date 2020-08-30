using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using System.Linq;

public enum GameState
{
    Prepare,
    Gaming,
    Succeed,
    Failed,
}

enum OperateType
{
    None,
    Move,
    LongTouchTile,
    ShortTouchTile,
    Scale,
}

public class InputControl : MonoBehaviour
{
    public GameObject TilePrefab;
    
    public GameObject TileParent;
    public Text LeftMine;
    public GameObject SettingPage;

    public AudioSource ButtonClickSound;
    public AudioSource OpenTileSound;

    private float MainOffsetX = 55.4f;
    private float MainOffsetY = -32;
    private float ViceOffsetX = -55.4f;
    private float ViceOffsetY = -32;

    private int Rows;
    private int Cols;
    private int MineTotalCount;
    private List<Tile> ReversedTiles;

    private Tile Active = null;
    private float TouchDownTime = 0;
    private Vector3 TouchDownPosition;
    private Vector3 TouchDownTileParentPosition;
    private Vector3[] TouchDownTilesCornerPosition = new Vector3[4];
    private OperateType OperateType;

    private GameState GameState = GameState.Prepare;
    private Tile FailedTile = null;
    private bool InitedMine = false;

    void Start()
    {
        resetTiles(9, 9, 10);
        resetStateNormal();
    }

    void resetTiles(int rows, int cols, int minecount)
    {
        for (int i = 0; i < TileParent.transform.childCount; i++)
        {
            Destroy(TileParent.transform.GetChild(i).gameObject);
        }

        Rows = rows;
        Cols = cols;
        MineTotalCount = minecount;
        ReversedTiles = new List<Tile>();

        for (int i = 0; i < rows; ++i)
        {
            Vector3 mainStartPos = new Vector3(i * ViceOffsetX, i * ViceOffsetY, 0);
            for (int j = 0; j < cols; j++)
            {
                GameObject obj = Instantiate(TilePrefab);
                obj.transform.SetParent(TileParent.transform, false);
                obj.transform.localPosition = mainStartPos + new Vector3(j * MainOffsetX, j * MainOffsetY, 0);

                Tile tile = obj.GetComponent<Tile>();
                tile.Row = i;
                tile.Col = j;
                tile.IsMine = false;

                ReversedTiles.Add(tile);
            }
        }

        Vector3 center = getPositionOf(rows / 2, cols / 2);
        TileParent.transform.localPosition = -1 * center;

        ReversedTiles.Reverse();
    }

    void resetMine(int startr, int startc)
    {
        int count = MineTotalCount;

        if (count >= Rows*Cols)
        {
            Debug.LogError("雷的数量过多了");
            return;
        }

        while (count > 0)
        {
            int mr = Random.Range(0, Rows);
            int mc = Random.Range(0, Cols);
            if (startr==mr && startc==mc)
                continue;

            Tile tile = GetTile(mr, mc);
            if (tile.IsMine)
                continue;

            tile.IsMine = true;
            --count;
        }

        for (int r = 0; r < Rows; r++)
        {
            for (int c = 0; c < Cols; c++)
            {
                int num = GetAroundMineCount(r, c);
                GetTile(r, c).Number = num;
            }
        }
    }

    void resetStateNormal()
    {
        ReversedTiles.ForEach((tile) => tile.Init());
        GameState = GameState.Gaming;
        LeftMine.text = MineTotalCount.ToString();
        SettingPage.SetActive(false);
        InitedMine = false;
    }

    int GetAroundMineCount(int centerr, int centerc)
    {
        int count = 0;
        for(int i=-1; i<=1; ++i)
        {
            for(int j=-1; j<=1; ++j)
            {
                if (i == 0 && j == 0)
                    continue;
                
                int r = i + centerr;
                int c = j + centerc;

                if (r < 0 || r >= Rows || c < 0 || c >= Cols)
                    continue;

                if (GetTile(r, c).IsMine)
                {
                    count += 1;
                }
            }
        }
        return count;
    }

    Tile GetTile(int r, int c)
    {
        return ReversedTiles[Rows * Cols - 1 - (r * Cols + c)];
    }

    Vector3 getPositionOf(int r, int c)
    {
        Vector3 mainStartPos = new Vector3(r * ViceOffsetX, r * ViceOffsetY, 0);
        return mainStartPos + new Vector3(c * MainOffsetX, c * MainOffsetY, 0);
    }

    public void Update()
    {
        if (Input.GetMouseButtonDown(0))
        {
            if (SettingPage.activeSelf)
                return;

            TouchDownTime = Time.realtimeSinceStartup;
            TouchDownPosition = Input.mousePosition;
            TouchDownTileParentPosition = TileParent.transform.localPosition;
            TouchDownTilesCornerPosition[0] = Camera.main.WorldToScreenPoint(ReversedTiles.Last().transform.position);
            TouchDownTilesCornerPosition[1] = Camera.main.WorldToScreenPoint(GetTile(0, Cols-1).transform.position);
            TouchDownTilesCornerPosition[2] = Camera.main.WorldToScreenPoint(ReversedTiles.First().transform.position);
            TouchDownTilesCornerPosition[3] = Camera.main.WorldToScreenPoint(GetTile(Rows-1, 0).transform.position);
            OperateType = OperateType.None;

            for(int i=0; i<TouchDownTilesCornerPosition.Length; ++i)
            {
                Debug.Log(string.Format("touchdown:{0}:{1}", i, TouchDownTilesCornerPosition[i].y));
            }

            if (GameState == GameState.Gaming)
            {
                Vector3 world = Camera.main.ScreenToWorldPoint(Input.mousePosition);

                Tile hittile = ReversedTiles.Find((t) => t.HitTest(world));
                if (!hittile)
                    return;

                Active = hittile;
                Active.Scaled = true;
            }
        }
        else if (Input.GetMouseButton(0))
        {
            if (TouchDownTime == 0)
                return;

            Vector3 world = Camera.main.ScreenToWorldPoint(Input.mousePosition);

            if (GameState != GameState.Prepare)
            {
                if ((Input.mousePosition - TouchDownPosition).magnitude > 10)
                {
                    OperateType = OperateType.Move;
                }
            }

            if (OperateType == OperateType.None)
            {
                if (GameState == GameState.Gaming)
                {
                    Tile hittile = ReversedTiles.Find((t) => t.HitTest(world));

                    if (Active && hittile == Active)
                    {
                        if (Time.realtimeSinceStartup - TouchDownTime > 0.5f)
                        {
                            OperateType = OperateType.LongTouchTile;
                        }
                    }
                    else
                    {
                        OperateType = OperateType.Move;
                    }
                }
            }

            if (OperateType == OperateType.Move)
            {
                if (Active)
                {
                    Active.Scaled = false;
                    Active = null;
                }

                MoveTileParent();
            }
            else if (OperateType == OperateType.LongTouchTile)
            {
                OnLongTouch(Active);

                Active.Scaled = false;
                Active = null;
                TouchDownTime = 0;
            }
        }
        else if (Input.GetMouseButtonUp(0))
        {
            if (TouchDownTime == 0)
                return;

            if (OperateType == OperateType.None)
            {
                if (GameState == GameState.Gaming && Active)
                {
                    OperateType = OperateType.ShortTouchTile;
                }
                else if (GameState == GameState.Succeed || GameState == GameState.Failed)
                {
                    SettingPage.SetActive(true);
                }
            }

            if (OperateType == OperateType.ShortTouchTile)
            {
                OnShortTouch(Active);

                Active.Scaled = false;
                Active = null;
            }
            else if (OperateType == OperateType.None)
            {
                if (GameState == GameState.Succeed || GameState == GameState.Failed)
                {
                    SettingPage.SetActive(true);
                }
            }

            TouchDownTime = 0;
            TouchDownPosition = Vector3.zero;
            OperateType = OperateType.None;
        }
    }

    private void MoveTileParent()
    {
        Vector3 delta = Input.mousePosition - TouchDownPosition;
        delta.z = 0;

        Debug.Log(string.Format("delta.y={0}", delta.y));

        delta.y = Mathf.Max(delta.y, Screen.height / 2 - TouchDownTilesCornerPosition[0].y);
        delta.y = Mathf.Min(delta.y, Screen.height / 2 - TouchDownTilesCornerPosition[2].y);
        delta.x = Mathf.Max(delta.x, Screen.width / 2 - TouchDownTilesCornerPosition[1].x);
        delta.x = Mathf.Min(delta.x, Screen.width / 2 - TouchDownTilesCornerPosition[3].x);
        
        TileParent.transform.localPosition = TouchDownTileParentPosition + delta;
    }

    private void OnShortTouch(Tile tile)
    {
        if (!InitedMine)
        {
            resetMine(tile.Row, tile.Col);
            InitedMine = true;
        }

        if (tile.State == TileState.Normal)
        {
            OpenTileSound.Play();

            OpenTile(tile.Row, tile.Col);
        }

        if (tile.State == TileState.Normal && tile.IsMine)
        {
            FailedTile = tile;
            SetGameState(GameState.Failed);
        }

        CheckSucceed();
    }

    private void OnLongTouch(Tile tile)
    {
        if (!InitedMine)
        {
            resetMine(tile.Row, tile.Col);
            InitedMine = true;
        }

        OpenTileSound.Play();

        SwitchFlag(tile);

        refreshLeftMine();

        CheckSucceed();
    }

    public void SwitchFlag(Tile tile)
    {
        if (Active.State == TileState.Normal)
        {
            Active.TrySetState(TileState.Flagged);
        }
        else if (Active.State == TileState.Flagged)
        {
            Active.TrySetState(TileState.Normal);
        }
    }

    public void OpenTile(int row, int col)
    {
        if (row<0 || row>=Rows || col<0 || col>=Cols)
            return;

        Tile tile = GetTile(row, col);
        if (tile.State == TileState.Normal && !tile.IsMine)
        {
            tile.TrySetState(TileState.Opened);

            if (tile.Number > 0)
            {
                return;
            }
        }
        else
        {
            return;
        }

        for (int i = -1; i <= 1; i++)
        {
            for (int j = -1; j <= 1; j++)
            {
                OpenTile(row + i, col + j);
            }
        }
    }

    public void SetGameState(GameState state)
    {
        if (state == GameState.Failed)
        {
            foreach (Tile tile in ReversedTiles)
            {
                tile.SetFailed(tile == FailedTile);
            }
        }

        GameState = state;
    }

    public int GetLeftMineCount()
    {
        int flagged = 0;
        foreach (Tile tile in ReversedTiles)
        {
            if (tile.State == TileState.Flagged)
            {
                flagged++;
            }
        }

        return MineTotalCount - flagged;
    }

    public void refreshLeftMine()
    {
        LeftMine.text = GetLeftMineCount().ToString();
    }

    public void OnClickSetting()
    {
        ButtonClickSound.Play();
        ButtonClickSound.Play();

        SettingPage.SetActive(!SettingPage.activeSelf);
    }

    public void OnClickRestart()
    {
        ButtonClickSound.Play();

        SettingPage.SetActive(false);

        resetTiles(Rows, Cols, MineTotalCount);
        resetStateNormal();
    }

    public void OnClick9x9()
    {
        ButtonClickSound.Play();

        SettingPage.SetActive(false);

        resetTiles(9, 9, 10);
        resetStateNormal();
    }

    public void OnClick16x16()
    {
        ButtonClickSound.Play();

        SettingPage.SetActive(false);

        resetTiles(16, 16, 40);
        resetStateNormal();
    }

    public void OnClick30x16()
    {
        ButtonClickSound.Play();

        SettingPage.SetActive(false);

        resetTiles(30, 16, 99);
        resetStateNormal();
    }

    public void OnClickSettingClose()
    {
        ButtonClickSound.Play();

        SettingPage.SetActive(false);
    }

    public void CheckSucceed()
    {
        bool succeed = false;
        
        int unopened = ReversedTiles.Count(tile => tile.State == TileState.Normal || tile.State == TileState.Flagged);
        if (unopened == MineTotalCount)
        {
            succeed = true;
        }

        if (!succeed)
        {
            succeed = true;
            foreach (Tile tile in ReversedTiles)
            {
                if (tile.IsMine)
                {
                    if (tile.State != TileState.Flagged)
                    {
                        succeed = false;
                        break;
                    }
                }
            }
        }

        if (succeed)
        {
            GameState = GameState.Succeed;
            ReversedTiles.ForEach(tile => tile.SetSucceed());
        }
    }

    
}
