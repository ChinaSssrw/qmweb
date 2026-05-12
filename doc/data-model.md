# 企盟小程序 — 数据模型

> 核心表结构设计。详细字段Schemas在开发时补充。

## 核心表总览

| 表名 | 说明 | 核心字段 |
|------|------|----------|
| users | 用户表 | id, wx_openid, nickname, avatar, phone, role, status, referrer_id, created_at |
| profiles | 名片表 | user_id, basic_info(JSON), contact_info(JSON), tags(JSON), bio(JSON), social(JSON), privacy_settings, version |
| status_posts | 动态状态条 | id, user_id, type(need/provide), content, is_pinned, created_at |
| friends | 好友关系 | id, user_a_id, user_b_id, status(pending/accepted), source(direct/activity), activity_id, created_at |
| activities | 活动表 | id, creator_id, title, description, start_time, end_time, location, max_participants, registration_deadline, space_id, status |
| activity_participants | 活动参与者 | id, activity_id, user_id, checked_in, checkin_time |
| spaces | 空间表 | id, manager_id, name, address, capacity, facilities(JSON), photos(JSON), price_per_hour, status |
| space_bookings | 空间预约 | id, space_id, user_id, activity_id, start_time, end_time, amount, status, payment_id |
| audit_records | 审核记录 | id, user_id, referrer_id, admin_id, referrer_status, admin_status, applied_at, completed_at |
| payments | 支付记录 | id, user_id, type(membership/space), amount, order_no, wx_pay_no, status, paid_at |
| interaction_stats | 互动统计 | id, user_a_id, user_b_id, co_occurrence_count, details(JSON array of activity_id+time) |

## 核心关系

```
users 1:N → profiles（用户有一个名片）
users 1:N → status_posts（用户有多个动态）
users M:N → friends（好友关系对等表）
users 1:N → activities（用户发起多个活动）
users M:N → activities → activity_participants（活动参与者）
activities N:1 → spaces（活动可选关联空间）
spaces 1:N → space_bookings（空间有多个预约）
users 1:1 → audit_records（用户有一条审核记录）
users 1:N → payments（用户有多个支付记录）
users M:N → interaction_stats（用户间互动统计）
```
