#!/bin/bash
# 每日同步脚本

echo "=========================================="
echo "🚀 开始每日同步工作流"
echo "=========================================="
echo ""

# 1. 同步 main 分支
echo "📥 1. 同步 main 分支..."
git checkout main
if [ $? -ne 0 ]; then
    echo "❌ 切换到 main 分支失败"
    exit 1
fi

git pull upstream main
if [ $? -ne 0 ]; then
    echo "❌ 从上游拉取代码失败"
    exit 1
fi

git push origin main
if [ $? -ne 0 ]; then
    echo "⚠️  推送到远程仓库失败（可能是网络问题，不影响本地同步）"
fi

echo "✅ main 分支同步完成！"
echo ""

# 2. 更新 adam 分支
echo "🔄 2. 更新 adam 分支..."
git checkout adam
if [ $? -ne 0 ]; then
    echo "❌ 切换到 adam 分支失败"
    exit 1
fi

git merge main
if [ $? -ne 0 ]; then
    echo "⚠️  合并出现冲突，请手动解决后运行："
    echo "   git add <冲突文件>"
    echo "   git commit"
    echo "   git push origin adam"
    exit 1
fi

git push origin adam
if [ $? -ne 0 ]; then
    echo "⚠️  推送 adam 分支失败"
    exit 1
fi

echo "✅ adam 分支更新完成！"
echo ""

# 3. 显示状态
echo "=========================================="
echo "📊 当前状态"
echo "=========================================="
echo "当前分支: $(git branch --show-current)"
echo ""
echo "远程仓库:"
git remote -v
echo ""
echo "最近的提交:"
git log --oneline -5
echo ""
echo "🎉 同步完成！可以开始工作了！"

