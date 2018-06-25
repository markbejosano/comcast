import sys
import os
import glob
import subprocess
import csv
from decimal import *

failed = 0
testcases = 0  # add on top (divider)
exec_counter = 0  # thissss
overall_passed = 0  # thissss


def main():
    try:
        file = os.stat("Data File.csv")
        if file.st_size == 0:
            print "Data File is Empty"
    except OSError:
        print "Data File.csv not Found"
        sys.exit(1)


def compare(calllog1, transfertype1, y, gen_result, gen_report):
    global overall_passed  # thisssss
    global failed
    global exec_counter  # thisss
    x = 0
    z = 0
    transfer = transfertype1.split(';')
    total_terms = len(transfer)
    global failed
    y = str(y)
    print "Test " + y + ": " + "For Call log " + calllog1
    total_terms = total_terms - 1
    alllines = set()
    found_prompt = set()
    not_found_prompt = set()
    while total_terms > x:
        flag = 0
        split_1 = transfer[x].split('=')
        first = split_1[0].lower().strip()
        second = split_1[1].strip()
        with open(calllog1) as calllog:
            verbiage = set()
            for line in calllog:
                if (first + ':' in line.lower() or first + '=' in line.lower()) and second in line:
                    verbiage.add(line)
                    alllines.add(line)
                    flag = 1
                elif first + ':' in line.lower() or first + '=' in line.lower():
                    verbiage.add(line)
                    alllines.add(line)

        if flag == 0:
            print transfer[x] + "\tWrong Value"
            not_found_prompt.add(transfer[x] + " Wrong Value or Not Found")
            z = 1
            failed = 1
        elif len(verbiage) == 0:
            print transfer[x] + "\tNot Found"
            failed = 1
            z = 1
        else:
            print transfer[x] + "\tFound"
            found_prompt.add(transfer[x] + " Found")
        print ''.join(verbiage)
        x += 1
    verbi = '<br/>'.join(alllines)
    prompi = '<br/>'.join(transfer)
    f_prompt = '<br/>'.join(found_prompt)
    nf_prompt = '<br/>'.join(not_found_prompt)
    if z == 1:
        print "                   STATUS: FAILED"
        gen_result.write(
            "<tr><td align='center'>" + y + "</td><td>" + prompi + "</td> <td>" + verbi + "</td>  <td>" + calllog1 + "</td> <td>" + nf_prompt + "</td> <td bgcolor='#e06745'>Failed</td></tr>")
        gen_report.write(
            "<tr><td align='center'>" + y + "</td><td>" + calllog1 + "</td> <td bgcolor='#e06745'>Failed </td></tr>")
    else:
        overall_passed += 1
        print "                   STATUS: PASSED"
        gen_result.write(
            "<tr><td align='center'>" + y + "</td><td>" + prompi + "</td> <td>" + verbi + "</td>   <td>" + calllog1 + "</td> <td>" + f_prompt + "</td> <td bgcolor='#99e26f'>Passed</td> </tr>")
        gen_report.write(
            "<tr><td align='center'>" + y + "</td><td>" + calllog1 + "</td> <td bgcolor='#99e26f'>Passed </td></tr>")
    exec_counter += 1


def excel():
    global gen_report
    global testcases  # thisss
    gen_result = open("KVPs Result.html", "a")
    gen_report = open("report.html", "a")
    gen_result.write("<html> <center><h1>Inbound Build Acceptance Automation</h1> <h3>Transfer Term</h3></center>")
    gen_report.write("<html><table align='center' border='1' width='70%'> </table>")
    gen_report.write("<br/><table align='center' width='35%'><tr><td align='center'><font size='4'><b>Transfer Term</b></font></td></tr></table>")
    z = 0
    with open('Data File.csv', 'rb') as f:
        reader = csv.reader(f)
        next(reader, None)
        y = 1;
        gen_result.write(
            "<table border='1' align='center'> <tr><td bgcolor='#c2c4c6' align='center'> <b>Test Case</b> </td> "
            "<td bgcolor='#c2c4c6' align='center'> <b>Transfer Term</b> </td> "
            "<td bgcolor='#c2c4c6' align='center'> <b>Actual Logs</b> </td> "
            "<td bgcolor='#c2c4c6' align='center'> <b>Call Logs</b> </td> "
            "<td bgcolor='#c2c4c6' align='center'> <b>Remarks</b> </td> "
            "<td bgcolor='#c2c4c6' align='center'> <b>Result</b> </td></tr>")
        gen_report.write(
            " <table border='1' align='center' width='35%'> <tr><td align='center' bgcolor='#c2c4c6' width='10%'> <b>Test Case</b> </td> "
            "<td align='center' bgcolor='#c2c4c6' width='60%'> <b>Call Log </b></td>"
            "<td align='center' bgcolor='#c2c4c6' width='20%'> <b>Pass/Fail </b></td></tr>")
        for line in reader:
            transfertype1 = line[1]
            calllog1 = line[2]
            if len(transfertype1) >= 5:
                if len(calllog1) >= 5:
                    compare(calllog1, transfertype1, y, gen_result, gen_report)
                    y += 1
    testcases = y - 1


if __name__ == "__main__":
    main()
    excel()
    print "EXEC COUNTER: ", exec_counter
    print "TEST CASES: ", testcases
    if exec_counter == testcases:
        getcontext().prec = 3
        percentage = Decimal(overall_passed) / Decimal(testcases) * 100
        totalper = str(percentage) + '%'
        gen_report.write(
            "</table><table align='center'> <tr><td><h3>Passed: " + totalper + "</h3></td></tr> </table>")
        writetime = open("writetime.txt","a")
        writetime.write("TransferType Percentage= " + totalper + "\n")
    if failed == 1:
        print"\n\n\n"
        raise SystemError('One of the Test Cases Failed')
