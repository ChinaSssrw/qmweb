# 企盟小程序 — Mock数据与测试夹具

> 所有测试用例使用的通用Mock数据和第三方服务模拟说明。

## 测试用户

| 用户 | openid | 角色 | 说明 |
|------|--------|------|------|
| test_user_a | mock_openid_a | 普通用户 | 有推荐人 |
| test_user_b | mock_openid_b | 普通用户 | 无好友 |
| test_user_c | mock_openid_c | 付费用户 | 审核通过 |
| test_admin | mock_openid_admin | 站点管理员 | 有审核权限 |

## Mock第三方服务

- **微信登录**：Mock返回固定openid和session_key
- **微信支付**：Mock返回固定支付单号，不调真实支付
- **语音识别**：Mock返回预设文本
- **文档解析**：Mock返回预设字段映射
