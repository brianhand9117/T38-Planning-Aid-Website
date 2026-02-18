# GitHub Repository Setup Guide

This guide walks you through creating a new GitHub repository and uploading your T-38 Planning Aid website code.

## Step 1: Create Repository on GitHub

1. **Go to GitHub**: https://github.com/new
2. **Log in** with your account (brianhand9117)
3. **Fill in the repository details**:
   - **Repository name**: `T38-Planning-Aid-Website` (or similar)
   - **Description**: "NASA-themed Flask web application for T-38 Planning Aid email subscription and monthly KML distribution"
   - **Public/Private**: Choose based on your preference (recommended: Public for portfolio)
   - **Initialize this repository with**: Leave UNCHECKED (we already have commits)
4. **Click "Create repository"**

## Step 2: Configure Git Remote

Replace `{your-username}` with `brianhand9117` and run these commands in your terminal:

```bash
cd C:\Users\bjhand\Downloads\Hand-T38_Planning_Aid-Fork-main\website

# Add remote repository
git remote add origin https://github.com/brianhand9117/T38-Planning-Aid-Website.git

# Verify remote was added
git remote -v
```

### Expected Output:
```
origin  https://github.com/brianhand9117/T38-Planning-Aid-Website.git (fetch)
origin  https://github.com/brianhand9117/T38-Planning-Aid-Website.git (push)
```

## Step 3: Push Code to GitHub

```bash
cd C:\Users\bjhand\Downloads\Hand-T38_Planning_Aid-Fork-main\website

# Push code to repository
git branch -M main
git push -u origin main
```

### First Time Push
- GitHub may prompt for authentication
- **Use a Personal Access Token** (recommended over password):
  1. Go to https://github.com/settings/tokens
  2. Click "Generate new token (classic)"
  3. Check boxes: `repo`, `read:user`
  4. Click "Generate token"
  5. **Copy the token** (you can only see it once)
  6. When git prompts for password, paste the token

### Alternative: SSH Authentication
If you prefer SSH:
```bash
# Configure SSH key first (if not already done)
ssh-keygen -t ed25519 -C "brianhand54@gmail.com"

# Then use SSH URL instead:
git remote set-url origin git@github.com:brianhand9117/T38-Planning-Aid-Website.git
```

## Step 4: Verify Upload

1. **Visit your repository**: https://github.com/brianhand9117/T38-Planning-Aid-Website
2. **Check that files are there**:
   - `app/` folder with source code
   - `requirements.txt`
   - `README.md` and documentation
   - `.env.example` (NOT `.env` - that's private!)
   - `Dockerfile`

## Step 5: Final Setup on GitHub

### Add Repository Description
1. Go to repository settings
2. Add description and topics
3. Recommended topics: `flask`, `python`, `email-subscription`, `automation`, `nasa`, `kml`

### Pin Important Files
Consider creating a GitHub wiki or pinning documents:
1. [QUICKSTART.md](QUICKSTART.md) - Quick setup guide
2. [EMAIL_TROUBLESHOOTING.md](EMAIL_TROUBLESHOOTING.md) - Email configuration help
3. [DEPLOYMENT.md](DEPLOYMENT.md) - Production deployment

## Quick Commands Reference

```bash
# Check git status
git status

# Check commits
git log --oneline

# Check remote
git remote -v

# Make changes and commit
git add .
git commit -m "Your message"
git push

# If you need to update a commit
git add .
git commit --amend
git push --force-with-lease
```

## Troubleshooting

### Error: "remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/brianhand9117/T38-Planning-Aid-Website.git
```

### Error: "Authentication failed"
- Make sure you're using a Personal Access Token, not your password
- Token should have `repo` permission
- Check that you're not including saved credentials from other accounts

### Error: "Permission denied (publickey)"
- SSH key issue - use HTTPS URL instead
- Or set up SSH key in GitHub: https://github.com/settings/keys

### Repository not showing files
- Check that the push completed: `git push -u origin main`
- Refresh the GitHub page
- Verify `.gitignore` is not excluding important files

## Future Updates

After the initial push, updating is simple:

```bash
git add .
git commit -m "Description of changes"
git push
```

## Next Steps

Once uploaded:
1. ✅ Share the repository link
2. ✅ Add badges to README (Python version, Flask version)
3. ✅ Set up GitHub Pages (if desired)
4. ✅ Create GitHub Issues for feature requests
5. ✅ Create GitHub Discussions if project grows

---

For help: Check GitHub documentation at https://docs.github.com/

