#!/bin/bash

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

show_menu() {
    clear
    echo -e "${CYAN}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║         VM ABSTRACTION LAB - MASTER CONTROL                 ║${NC}"
    echo -e "${CYAN}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo
    echo -e "${GREEN}ABSTRACTION LEVELS:${NC}"
    echo "  0) Level 0 - Basic Process"
    echo "  1) Level 1 - Docker Container"
    echo "  2) Level 2 - Docker Compose"
    echo "  3) Level 3 - Kubernetes"
    echo "  4) Level 4 - Virtual Machines"
    echo "  5) Level 5 - Nested Virtualization"
    echo "  6) Level 6 - Cloud Simulation"
    echo
    echo -e "${BLUE}CONTROL OPTIONS:${NC}"
    echo "  a) Start ALL levels"
    echo "  s) Stop ALL levels"
    echo "  m) Launch Monitoring"
    echo "  t) Show Status"
    echo "  l) View Logs"
    echo "  q) Quit"
    echo
    echo -n "Select option: "
}

start_level() {
    case $1 in
        0)
            echo -e "${GREEN}Starting Level 0 - Basic Process...${NC}"
            cd level-0-process
            python3 simple_server.py &
            cd ..
            ;;
        1)
            echo -e "${GREEN}Starting Level 1 - Docker Container...${NC}"
            cd level-1-container
            ./run.sh
            cd ..
            ;;
        2)
            echo -e "${GREEN}Starting Level 2 - Docker Compose...${NC}"
            cd level-2-compose
            docker-compose up -d
            cd ..
            ;;
        3)
            echo -e "${GREEN}Starting Level 3 - Kubernetes...${NC}"
            cd level-3-kubernetes
            ./deploy.sh
            cd ..
            ;;
        4)
            echo -e "${GREEN}Starting Level 4 - Virtual Machines...${NC}"
            cd level-4-vm
            ./manage.sh start
            cd ..
            ;;
        5)
            echo -e "${GREEN}Starting Level 5 - Nested Virtualization...${NC}"
            cd level-5-nested
            docker-compose up -d
            cd ..
            ;;
        6)
            echo -e "${GREEN}Starting Level 6 - Cloud Simulation...${NC}"
            cd level-6-cloud
            ./deploy.sh
            cd ..
            ;;
        all)
            for i in {0..6}; do
                start_level $i
                sleep 2
            done
            ;;
    esac
}

stop_level() {
    case $1 in
        0)
            echo -e "${RED}Stopping Level 0...${NC}"
            pkill -f simple_server.py
            ;;
        1)
            echo -e "${RED}Stopping Level 1...${NC}"
            docker stop level-1-app
            docker rm level-1-app
            ;;
        2)
            echo -e "${RED}Stopping Level 2...${NC}"
            cd level-2-compose
            docker-compose down
            cd ..
            ;;
        3)
            echo -e "${RED}Stopping Level 3...${NC}"
            kubectl delete -f level-3-kubernetes/deployment.yaml
            minikube stop
            ;;
        4)
            echo -e "${RED}Stopping Level 4...${NC}"
            cd level-4-vm
            ./manage.sh stop
            cd ..
            ;;
        5)
            echo -e "${RED}Stopping Level 5...${NC}"
            cd level-5-nested
            docker-compose down
            cd ..
            ;;
        6)
            echo -e "${RED}Stopping Level 6...${NC}"
            cd level-6-cloud
            docker-compose down
            cd ..
            ;;
        all)
            for i in {0..6}; do
                stop_level $i
            done
            ;;
    esac
}

show_status() {
    echo -e "${CYAN}═══ System Status ═══${NC}"
    
    # Check Level 0
    if pgrep -f simple_server.py > /dev/null; then
        echo -e "Level 0: ${GREEN}●${NC} Running"
    else
        echo -e "Level 0: ${RED}●${NC} Stopped"
    fi
    
    # Check Level 1
    if docker ps | grep -q level-1-app; then
        echo -e "Level 1: ${GREEN}●${NC} Running"
    else
        echo -e "Level 1: ${RED}●${NC} Stopped"
    fi
    
    # Check Level 2
    if docker ps | grep -q level2; then
        echo -e "Level 2: ${GREEN}●${NC} Running"
    else
        echo -e "Level 2: ${RED}●${NC} Stopped"
    fi
    
    # Check Level 3
    if kubectl get pods 2>/dev/null | grep -q level3; then
        echo -e "Level 3: ${GREEN}●${NC} Running"
    else
        echo -e "Level 3: ${RED}●${NC} Stopped"
    fi
    
    # Check Level 4
    if vagrant status 2>/dev/null | grep -q running; then
        echo -e "Level 4: ${GREEN}●${NC} Running"
    else
        echo -e "Level 4: ${RED}●${NC} Stopped"
    fi
    
    # Check Level 5
    if docker ps | grep -q level5; then
        echo -e "Level 5: ${GREEN}●${NC} Running"
    else
        echo -e "Level 5: ${RED}●${NC} Stopped"
    fi
    
    # Check Level 6
    if docker ps | grep -q localstack; then
        echo -e "Level 6: ${GREEN}●${NC} Running"
    else
        echo -e "Level 6: ${RED}●${NC} Stopped"
    fi
    
    echo
    echo -e "${BLUE}Access URLs:${NC}"
    echo "  Level 0: http://localhost:8000"
    echo "  Level 1: http://localhost:3001"
    echo "  Level 2: http://localhost:3002"
    echo "  Level 3: $(minikube service level3-service --url 2>/dev/null || echo 'Not running')"
    echo "  Level 4: http://localhost:3004"
    echo "  Level 5: http://localhost:3005"
    echo "  Level 6: http://localhost:3006"
    echo "  Monitoring: http://localhost:3000 (Grafana)"
}

# Main loop
while true; do
    show_menu
    read -r choice
    
    case $choice in
        [0-6])
            start_level $choice
            ;;
        a)
            start_level all
            ;;
        s)
            stop_level all
            ;;
        m)
            cd monitoring
            docker-compose up -d
            cd ..
            echo -e "${GREEN}Monitoring started at http://localhost:3000${NC}"
            ;;
        t)
            show_status
            ;;
        l)
            echo "Select level for logs (0-6): "
            read -r level
            case $level in
                1) docker logs -f level-1-app ;;
                2) cd level-2-compose && docker-compose logs -f && cd .. ;;
                3) kubectl logs -f deployment/level3-app ;;
                *) echo "Logs not available for this level" ;;
            esac
            ;;
        q)
            echo -e "${YELLOW}Shutting down...${NC}"
            stop_level all
            exit 0
            ;;
        *)
            echo -e "${RED}Invalid option${NC}"
            sleep 2
            ;;
    esac
    
    echo
    echo "Press Enter to continue..."
    read
done
