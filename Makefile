PY = python3
CRON_SCRIPT := /home/vboxuser/EMAIL_READER_AGENT/agent_scheduler.sh
CRON_JOB := 0 12 * * * $(CRON_SCRIPT)

# Run cleanup script
clean: cleanup.py
	$(PY) cleanup.py


cleanup.py: get_today_email
	echo "Define cleanup.py file first"

get_today_email:
	echo "done"

add_cron_job: agent_scheduler.sh
	chmod +x $(CRON_SCRIPT)
	@echo "Adding cron job for $(CRON_SCRIPT)..."
	@crontab -l 2>/dev/null | grep -v "$(CRON_SCRIPT)" > temp_cron || true
	@echo "$(CRON_JOB)" >> temp_cron
	@crontab temp_cron
	@rm -f temp_cron
	@echo "Cron job installed:"
	@crontab -l | grep -F "$(CRON_SCRIPT)"


remove_old_cron_job:
	@echo "Removing existing cron job for $(CRON_SCRIPT)..."
	@crontab -l 2>/dev/null | grep -v "$(CRON_SCRIPT)" > temp_cron || true
	@crontab temp_cron
	@rm -f temp_cron
	@echo "Old cron job removed."


force_add_cron_job:
	$(MAKE) remove_old_cron_job
	$(MAKE) add_cron_job


agent_scheduler.sh:
	@echo "First create the scheduler script"

git_pusher:
#@ - to supress make file's default echo and ; to chain to next command - \ command block line continuation
	@echo "Enter Commit message:"; \
	read msg; \
	git add .; \
	git commit -m "$$msg"; \
	git push