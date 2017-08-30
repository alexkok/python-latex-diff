from subprocess import call
import sys, os

# Settings
workingDir =  "build"
removeOld = True;
gitUrl = "GIT_URL"
startDirPrefix = "start"
endDirPrefix = "end"
firstCommitHash = "HASH_START"  # Specific commit hash for diff
secondCommitHash = "HASH_END" # HEAD also possible
mainTexFile = "MAIN_TEX_FILE"
runLocation = repr(os.getcwd())


# Functions
def getDirForCommit( tag, commitHash ):
	return workingDir + "/" + tag + "_" + commitHash

def buildLatex(directory):
	pdflatexCommand = ["cd", directory, "&", "pdflatex", "-interaction=nonstopmode", mainTexFile];
	bibtexCommand = ["cd", directory, "&", "bibtex", mainTexFile];
	print(pdflatexCommand)
	print(runLocation)

	print("> Executing pdflatex");
	call(pdflatexCommand, shell=True)
	print("> Executing bibtex");
	call(bibtexCommand, shell=True)
	print("> Executing pdflatex");
	call(pdflatexCommand, shell=True)
	print("> Executing pdflatex");
	call(pdflatexCommand, shell=True)

def checkOutCommit( tag, commitHash ):
	commitDir = getDirForCommit(tag, commitHash)
	print("> Creating directory for commit. Path: " + commitDir)
	call(["mkdir", commitDir]) # Making dir

	print("> Cloning reposirory")
	call(["git", "clone", "-n", gitUrl, commitDir])        # Checking out initial repo
	
	print("> Checking out with commit: " + commitHash + ". In directory: " + commitDir)
	call(["git", "--git-dir=" + commitDir + "/.git", "--work-tree=" + commitDir, "checkout", commitHash]) # Checkout to the right commit

	print("> Building latex files")
	buildLatex(commitDir)


# The execution
print("** Settings **")
print("- Running directory:  " + runLocation)
print("- Working directory:  " + workingDir)
print("- Git url:            " + gitUrl)
print("- First commit hash:  " + firstCommitHash)
print("- Second commit hash: " + secondCommitHash)
print("- Main tex file:      " + mainTexFile)

print("** Phase 1: Setup build folder **")
print("> Removing old build folder")
call(["rm", "-rf", workingDir])

print("> Creating build folder")
call(["mkdir", workingDir])

print("** Phase 2: Checking out repositories **")
print("> Checking out start commit")
checkOutCommit(startDirPrefix, firstCommitHash)

print("> Checking out end commit")
checkOutCommit(endDirPrefix, secondCommitHash)

print("** Phase 3: Running latex-diff **")
resultDir = getDirForCommit("", "result");
print("> Creating result dir: " + resultDir)
call(["mkdir", resultDir])

endDir = getDirForCommit(endDirPrefix, secondCommitHash);
startTexFile = getDirForCommit(startDirPrefix, firstCommitHash) + "/" + mainTexFile + ".tex"
endTexFile =  endDir + "/" + mainTexFile + ".tex"
resultingTexFile = resultDir + "/" + mainTexFile + ".tex"
print("> Calling latexdiff")
print("> - Start:  " + startTexFile)
print("> - End:    " + endTexFile)
print("> - Result: " + resultingTexFile)
call(["latexdiff", "--flatten", "--verbose", startTexFile, endTexFile, ">", resultingTexFile], shell=True)

print("** Phase 4: Copying additional required files **")
print("> Copying figures")
call(["cp", "-R", endDir + "/figures", resultDir + "/figures"], shell=True)
print("> Copying template .cls file")
call(["cp", endDir + "/uvamscse.cls", resultDir + "/uvamscse.cls"], shell=True)

print("** Phase 5: Building latex document **")
print("> Building latex files")
buildLatex(resultDir)
