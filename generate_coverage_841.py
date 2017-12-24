"""=============================

THIS IS CURRENTLY VERY UNFINISHED AND UNEXTENSIBLE. I MADE IT TO IMMEDIATELY
TACKLE THE PROBLEM I HAD TO SOLVE. IT ACTUALLY ONLY WORKS FROM THE DIRECTORY
ABOVE (OOPS). I'LL MODIFY IT TO MAKE IT MORE USEFUL EVENTUALLY.

================================

compile instructions for each source file
gcc-7 -std=c99 -fprofile-arcs -ftest-coverage -g -w replace/versions.alt/versions.orig/v[number]/replace.c -o source/replace.v[number].exe

================================

location of source files:
replace/versions.alt/versions.orig/v[number]/

================================

example line in replace/scripts/runall.sh:
../source/replace.exe '-?' 'a&'  < ../inputs/temp-test/1.inp.1.1 > ../outputs/t1
want to make it:
../source/replace.v[number].exe '-?' 'a&'  < ../inputs/temp-test/1.inp.1.1 > ../outputs/v[number]/t1

================================

need to see if:
replace/outputs/t1 != replace/outputs/v[number]/t1
if so then t is true (when it fails)

================================

for each source file
    compile source file
        for each test
            run test
            compare test output to correct output
            run gcov on source
            parse .gcov file to file of test stuff
            delete .gcda file

============================="""

import subprocess
CWD_PREFIX="replace/versions.alt/versions.orig/v"

def comp(version):
    """
    compile the version
    """
    subprocess.run(["gcc-7", "-std=c99", "-fprofile-arcs", "-ftest-coverage",
    "-g", "-w", "replace.c", "-o",
    "../../../source/replace.v" + str(version) + ".exe"],
    cwd=CWD_PREFIX+str(version))

def format_test(version, line, num):
    """
    format and return a corrected version of the test line
    """
    line = line.split()
    ####line[ 0] = "../../../source/replace.v" + str(version) + ".exe"
    ####line[-3] = "replace" + line[-3][2:]
    ####line[-1] = "replace/outputs/v" + str(version) + "/" + line[-1].split('/')[-1]
    line = ["../../../source/replace.v" + str(version) + ".exe"] + line
    line[-1] = "replace/inputs/" + line[-1]
    line.append(">")
    line.append("replace/outputs/v" + str(version) + "/t" + str(num)) 
    return(line)#line[0], ' '.join(line[1:])])

def fail_check(version, num):
    """
    compare the first (and only) line of the control output and version output
    return true if they differ (test failed) and false if it passed
    """
    f1 = open("replace/outputs/t" + str(num), 'r')
    f2 = open("replace/outputs/v" + str(version) + "/t" + str(num), 'r')
    ret = f1.readlines() != f2.readlines()
    f1.close()
    f2.close()
    return ret

def gcov_it(version, num):
    """
    parse the coverage output to make FOL statements
    returns a list of FOL statements
    """
    subprocess.run(["gcov-7", "-i", "replace.c"],
            cwd=CWD_PREFIX+str(version))
    gcov = open("replace/versions.alt/versions.orig/v" + str(version) +
        "/replace.c.gcov", 'r')
    out = []
    for line in gcov:
        info = line.split(':')[1].split(',')
        if line[0]=='l' and int(info[1]):
            out.append("cover(T{},S{})".format(str(num), info[0]))
    gcov.close()
    subprocess.run(["rm", "replace/versions.alt/versions.orig/v" +
        str(version) + "/replace.gcda"])
    return out

def start():
    """
    compile the version
    """
    subprocess.run(["gcc-7", "-std=c99", "-fprofile-arcs", "-ftest-coverage",
        "-g", "-w", "replace.c", "-o",
        "../../source/replace.exe"], cwd="replace/source.alt/source.orig")
    
    script_file = open("replace/testplans.alt/suite1", 'r')
    for num, line in enumerate(script_file.readlines()):
        num += 1
        if num != 16:
            continue
        #print("Generating control test {}".format(num))
        #format the line correctly and run the test
        test = format_test(0, line.strip(), num)
        #if test[-3].split('/')[2] != "temp-test":
        #    continue
        in_test = open(test[-3], 'r')
        out_test = open("replace/outputs/t" + str(num), 'w')
        subprocess.run(["../../source/replace.exe"]+test[1:-4],
            stdin=in_test, stdout=out_test,
            cwd="replace/source.alt/source.orig")
        in_test.close()
        out_test.close()
        subprocess.run(["rm", "replace/source.alt/source.orig/replace.gcda"])
 
def main():
    #try:
    #    pass#subprocess.run(["rm", "-r", "replace/outputs/v*"])
    #except:
    #    pass
    #for each version in the given range...
    start()
    cov_lines = open("jfmc.db", 'r').readlines()
    for version in range(1, 33):
        out_file = open("coverage_small" +  str(version) + ".db", 'w')
        try:
            subprocess.run(["mkdir", "replace/outputs/v" + str(version)])
        except:
            pass
        #compile it
        comp(version)
        #open the script file
        ####script_file = open("replace/scripts/runall.sh", 'r')
        script_file = open("replace/testplans.alt/suite1", 'r')
        #for every line in the script file...
        for num, line in enumerate(script_file.readlines()):
            #if line is odd or 0, it's just diagnostic
            ####if num % 2 or not num:
            ####    pass#subprocess.run([line.split()[0],' '.join(line.strip().split()[1:])])
            #otherwise, gotta do more
            #else:
                #correct num
                ####num //= 2
                num += 1
                if num != 16:
                    continue
                #print("Generating test {} for version {}".format(num, version))
                #format the line correctly and run the test
                test = format_test(version, line.strip(), num)
                #if test[-3].split('/')[2] != "temp-test":
                #    continue
                in_test = open(test[-3], 'r')
                out_test = open(test[-1], 'w')
                #try:
                subprocess.run(test[:-4], stdin=in_test, stdout=out_test,
                        cwd=CWD_PREFIX+str(version))
                #except:
                    #subprocess.run(["mkdir", "replace/outputs/v" + str(version)])
                    #subprocess.run(test[:-4], stdin=in_test, stdout=out_test,
                    #    cwd=CWD_PREFIX+str(version))
                in_test.close()
                out_test.close()
                #determine if the test failed
                test_fails = fail_check(version, num)
                out_file.write(("" if test_fails else "!") + "failed(T" +
                    str(num) + ')\n')
                #run gcov, parse that file, then remove the .gcda file
                out_file.write('\n'.join(gcov_it(version, num)) + '\n')
        line = str(subprocess.Popen(
            ["diff", "replace/source.alt/source.orig/replace.c",
            "replace/versions.alt/versions.orig/v" + str(version) + "/replace.c"],
            stdout=subprocess.PIPE).stdout.readline())
        if version < 23:
            out_file.write("buggy(S"+line.split('c')[0][2:]+')\n')
        out_file.write(''.join(cov_lines))
        out_file.close()

if __name__ == "__main__":
    main()
