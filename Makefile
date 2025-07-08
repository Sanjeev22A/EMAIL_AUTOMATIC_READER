PY = python3
CRON_SCRIPT := /home/vboxuser/EMAIL_READER_AGENT/agent_scheduler.sh
CRON_JOB := 0 8 * * * $(CRON_SCRIPT)
clean: cleanup.py
	$(PY) cleanup.py

cleanup.py: get_today_email
	echo "Define cleanup.py file first"

get_today_email:
	echo "done"

##make file in progress, will complete it once project is done
##Will 

##Make the script executable
##have added the script itself as depedency, will later write a resolution script
add_cron_job:agent_scheduler.sh 
	chmod +x agent_scheduler.sh 
	@echo "Checking if cron job already exists..."
	@crontab -l 2>/dev/null | grep -F "$(SCRIPT_PATH)" >/dev/null && \
		echo "Cron job already exists." || \
		(crontab -l 2>/dev/null; echo "$(CRON_JOB)") | crontab -
	@echo "Cron job Successfully installed"
	@crontab -l | grep -F "$(SCRIPT_PATH)"

agent_scheduler.sh:
	echo "First create the scheduler script"

