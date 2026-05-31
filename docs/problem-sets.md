# 题单 API

## 列出题单

<table>
  <tr>
    <th align="right">请求</th>
    <td><code>GET /training/list</code></td>
  </tr>
  <tr>
    <th align="right">参数</th>
    <td><code>ProblemSetListParams</code></td>
  </tr>
  <tr>
    <th align="right">响应主体</th>
    <td><code>application/json</code> (<code>LentilleDataResponse&lt;ProblemSetListData&gt;</code>)</td>
  </tr>
</table>

返回当前分类下的题单列表。`data` 包含以下字段：

- `trainings` — 题单分页列表（官方题单 perPage=18，精选题单 perPage=30）
- `acCounts` — 当前用户在各题单中已通过的题目数，键为题单 ID（字符串）
- `type` — 当前分类 key（如 `"srqc-jc"`、`"contest.noip"`）
- `categories` — 所有可用分类列表，每项包含 `key` 和 `name`

## 列出创建的题单

<table>
  <tr>
    <th align="right">请求</th>
    <td><code>GET /api/user/createdTrainings</code></td>
  </tr>
  <tr>
    <th align="right">参数</th>
    <td><code>{ page?: number }</code></td>
  </tr>
  <tr>
    <th align="right">响应主体</th>
    <td><code>application/json</code> (<code>{ trainings: List&lt;ProblemSet&gt; }</code>)</td>
  </tr>
</table>

## 获取题单

<table>
  <tr>
    <th align="right">请求</th>
    <td><code>GET /training/:id</code></td>
  </tr>
  <tr>
    <th align="right">响应主体</th>
    <td><code>application/json</code> (<code>LentilleDataResponse&lt;ProblemSetData&gt;</code>)</td>
  </tr>
</table>

`data` 包含以下字段：

- `training` — 题单详情（`ProblemSetDetails`），其中 `problems` 为 `TrainingProblem[]`，每项直接包含题目信息（`pid`、`name`、`difficulty`、`submitted`、`accepted`、`tags`、`provider` 等），而非嵌套在 `problem` 键下
- `canEdit` — 当前用户是否可编辑此题单
- `privilegedTeams` — 有权限的团队列表（仅对有编辑权限的用户返回）

## 列出收藏的题单

<table>
  <tr>
    <th align="right">请求</th>
    <td><code>GET /api/user/markedTrainings</code></td>
  </tr>
  <tr>
    <th align="right">参数</th>
    <td><code>{ page?: number }</code></td>
  </tr>
  <tr>
    <th align="right">响应主体</th>
    <td><code>application/json</code> (<code>{ trainingParticipations: List&lt;{ training: ProblemSet; user: UserSummary }&gt; }</code>)</td>
  </tr>
</table>

## 收藏题单

<table>
  <tr>
    <th align="right">请求</th>
    <td><code>POST /api/training/mark/:id</code></td>
  </tr>
  <tr>
    <th align="right">响应主体</th>
    <td><code>application/json</code> (<code>{}</code>)</td>
  </tr>
</table>

## 取消收藏题单

<table>
  <tr>
    <th align="right">请求</th>
    <td><code>POST /api/training/unmark/:id</code></td>
  </tr>
  <tr>
    <th align="right">响应主体</th>
    <td><code>application/json</code> (<code>{}</code>)</td>
  </tr>
</table>

## 创建题单

<table>
  <tr>
    <th align="right">请求</th>
    <td><code>POST /api/training/new</code></td>
  </tr>
  <tr>
    <th align="right">请求主体</th>
    <td><code>application/json</code> (<code>{ settings: ProblemSetSettings; providerID: number | null }</code>)</td>
  </tr>
  <tr>
    <th align="right">响应主体</th>
    <td><code>application/json</code> (<code>{ id: number }</code>)</td>
  </tr>
</table>

## 编辑题单

<table>
  <tr>
    <th align="right">请求</th>
    <td><code>POST /api/training/edit/:id</code></td>
  </tr>
  <tr>
    <th align="right">请求主体</th>
    <td><code>application/json</code> (<code>{ settings: ProblemSetSettings }</code>)</td>
  </tr>
  <tr>
    <th align="right">响应主体</th>
    <td><code>application/json</code> (<code>{ id: number }</code>)</td>
  </tr>
</table>

## 添加题单题目

<table>
  <tr>
    <th align="right">请求</th>
    <td><code>POST /api/training/addProblem/:id</code></td>
  </tr>
  <tr>
    <th align="right">请求主体</th>
    <td><code>application/json</code> (<code>{ pids: string[] }</code>)</td>
  </tr>
  <tr>
    <th align="right">响应主体</th>
    <td><code>application/json</code> (<code>{ addedProblems: string[] }</code>)</td>
  </tr>
</table>

## 编排题单题目

<table>
  <tr>
    <th align="right">请求</th>
    <td><code>POST /api/training/editProblems/:id</code></td>
  </tr>
  <tr>
    <th align="right">请求主体</th>
    <td><code>application/json</code> (<code>{ pids: string[] }</code>)</td>
  </tr>
  <tr>
    <th align="right">响应主体</th>
    <td><code>application/json</code> (<code>{}</code>)</td>
  </tr>
</table>

## 转存题单

<table>
  <tr>
    <th align="right">请求</th>
    <td><code>POST /api/training/clone/:id</code></td>
  </tr>
  <tr>
    <th align="right">请求主体</th>
    <td><code>application/json</code> (<code>{ type: number; providerID: number | null }</code>)</td>
  </tr>
  <tr>
    <th align="right">响应主体</th>
    <td><code>application/json</code> (<code>{}</code>)</td>
  </tr>
</table>

## 删除题单

<table>
  <tr>
    <th align="right">请求</th>
    <td><code>POST /api/training/delete/:id</code></td>
  </tr>
  <tr>
    <th align="right">响应主体</th>
    <td><code>application/json</code> (<code>{}</code>)</td>
  </tr>
</table>
