# 企盟小程序 — API接口契约

> 所有API返回统一格式：`{"code": 0, "data": ..., "message": "ok"}`

## 认证与用户

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/auth/wx-login | 微信登录（code → token+用户信息） |
| POST | /api/auth/register | 注册（手机号+推荐人ID → 用户） |

## 名片

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/profile | 获取当前用户名片 |
| PUT | /api/profile | 手动编辑提交更新名片 |
| POST | /api/profile/voice | 语音输入（音频→转文字→NLP分类填充） |
| POST | /api/profile/document | 文档上传解析 |

## 动态状态条

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/status | 获取动态列表 |
| PUT | /api/status | 发布/编辑/置顶 |
| DELETE | /api/status/{id} | 删除 |

## 好友

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/friends | 好友列表 |
| POST | /api/friends/request | 发送好友申请 |
| POST | /api/friends/accept | 同意好友申请 |

## 活动

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/activities | 活动列表（分页） |
| POST | /api/activities | 发起活动（校验付费身份） |
| POST | /api/activities/{id}/register | 报名 |
| POST | /api/activities/{id}/checkin | 签到打卡 |
| GET | /api/activities/{id}/circle | 共同活动圈 |
| POST | /api/activities/ai-assist | AI辅助生成活动内容 |

## 空间

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/spaces | 空间列表 |
| POST | /api/spaces | 上架空间（空间管理者） |
| POST | /api/spaces/{id}/book | 预约空间 |
| GET | /api/spaces/{id}/slots | 可预约时段 |

## 支付

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/payments/membership | 会员升级支付 |
| POST | /api/payments/space-booking | 空间预约支付 |
| POST | /api/payments/notify | 微信支付回调通知 |

## 审核

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/membership/apply | 提交升级申请 |
| POST | /api/audit/review | 审核通过/驳回 |
| GET | /api/membership/status | 查询会员状态 |

## 统计

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/statistics/interaction | 互动统计列表 |
| GET | /api/statistics/interaction/{userId} | 与指定用户的互动详情 |
