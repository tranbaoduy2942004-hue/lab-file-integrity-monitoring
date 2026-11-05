# Linux File Integrity Monitoring

Lab ID: lab-file-integrity-monitoring

## Topology
- linux-host: 172.29.115.10
- soc: 172.29.115.20
- Network: FILE_INTEGRITY_NET
- Evidence API: HTTP 8080

## Objectives
1. Establish a trusted file baseline.
2. Simulate unauthorized file modification.
3. Collect file integrity evidence.
4. Detect changes using SHA-256.
5. Restore and verify the original file.

## Installation (HOST)
imodule https://raw.githubusercontent.com/tranbaoduy2942004-hue/lab-file-integrity-monitoring/main/imodule.tar
labtainer lab-file-integrity-monitoring

## Practice

### Linux Host: Establish baseline
bash /usr/local/bin/manage_fim.sh baseline

### Linux Host: Simulate unauthorized change
bash /usr/local/bin/manage_fim.sh tamper
bash /usr/local/bin/manage_fim.sh status

### SOC: Collect and detect
python3 /usr/local/bin/soc_fim.py collect
python3 /usr/local/bin/soc_fim.py detect

### Linux Host: Restore
bash /usr/local/bin/manage_fim.sh restore

### SOC: Verify recovery
python3 /usr/local/bin/soc_fim.py verify

### HOST: Checkwork
checkwork lab-file-integrity-monitoring

Expected: 5/5 Y

## Safety
All activities are isolated inside Docker containers.
Only a simulated configuration file is modified.
