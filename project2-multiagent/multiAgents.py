# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

from collections import deque
import random

from util import manhattanDistance
import util
from game import Agent, Directions, Actions
from pacman import GameState


def _nearestFoodPathDistance(position, food, walls):
    """Tìm đường đi ngắn nhất đến thức ăn qua các ô hợp lệ (BFS)."""
    start = (int(position[0]), int(position[1]))
    if food[start[0]][start[1]]:
        return 0

    queue = deque([(start[0], start[1], 0)])
    visited = {start}
    width, height = walls.width, walls.height

    while queue:
        x, y, distance = queue.popleft()
        next_distance = distance + 1
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if (0 <= nx < width and 0 <= ny < height
                    and not walls[nx][ny] and (nx, ny) not in visited):
                if food[nx][ny]:
                    return next_distance
                visited.add((nx, ny))
                queue.append((nx, ny, next_distance))

    return float('inf')


# Bộ nhớ đệm: mỗi bố cục dùng chung bảng khoảng cách để không chạy BFS
# lặp lại ở hàng nghìn nút lá của Expectimax.
_MAZE_DISTANCE_CACHE = {}


def _distancesFrom(position, walls):
    """Trả về khoảng cách đường đi ngắn nhất từ một ô đến các ô hợp lệ."""
    key = id(walls)
    entry = _MAZE_DISTANCE_CACHE.get(key)
    if entry is None or entry[0] is not walls:
        # Giới hạn số bố cục lưu để bộ nhớ không tăng vô hạn.
        if len(_MAZE_DISTANCE_CACHE) >= 8:
            _MAZE_DISTANCE_CACHE.pop(next(iter(_MAZE_DISTANCE_CACHE)))
        # Giữ tham chiếu walls để tránh trùng id nếu bố cục cũ bị giải phóng.
        entry = (walls, {})
        _MAZE_DISTANCE_CACHE[key] = entry

    distances_by_source = entry[1]
    if position in distances_by_source:
        return distances_by_source[position]

    queue = deque([position])
    distances = {position: 0}
    width, height = walls.width, walls.height
    while queue:
        x, y = queue.popleft()
        new_distance = distances[(x, y)] + 1
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if (0 <= nx < width and 0 <= ny < height
                    and not walls[nx][ny] and (nx, ny) not in distances):
                distances[(nx, ny)] = new_distance
                queue.append((nx, ny))

    distances_by_source[position] = distances
    return distances


class ReflexAgent(Agent):
    """Tác nhân phản xạ: đánh giá từng hành động mà không duyệt cây tìm kiếm."""

    def getAction(self, gameState: GameState):
        legalMoves = gameState.getLegalActions()
        if not legalMoves:
            return Directions.STOP

        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [i for i, score in enumerate(scores) if score == bestScore]
        return legalMoves[random.choice(bestIndices)]

    def evaluationFunction(self, currentGameState: GameState, action):
        """Đánh giá cặp (trạng thái hiện tại, hành động đề xuất) - Q1."""
        successor = currentGameState.generatePacmanSuccessor(action)
        if successor.isWin():
            return successor.getScore() + 1000000
        if successor.isLose():
            return successor.getScore() - 1000000

        position = successor.getPacmanPosition()
        food = successor.getFood()
        remaining_food = food.asList()
        ghosts = successor.getGhostStates()
        capsules = successor.getCapsules()

        score = float(successor.getScore())

        # Thưởng khi ăn thức ăn ngay lập tức; ưu tiên quét hết bản đồ.
        # BFS tính khoảng cách đường đi thực, không xuyên tường trong mê cung.
        eaten = currentGameState.getNumFood() - len(remaining_food)
        score += 55.0 * eaten - 5.0 * len(remaining_food)
        if remaining_food:
            food_distance = _nearestFoodPathDistance(position, food, successor.getWalls())
            if food_distance != float('inf'):
                score -= 1.6 * food_distance
                score += 10.0 / (food_distance + 1.0)

        # Tránh ma nguy hiểm; chỉ đuổi ma đang hoảng loạn khi còn đủ thời gian.
        active_ghost_nearby = False
        for ghost in ghosts:
            distance = manhattanDistance(position, ghost.getPosition())
            if ghost.scaredTimer > distance + 1:
                score += 55.0 / (distance + 1.0)
            else:
                if distance <= 1:
                    score -= 250.0
                elif distance <= 2:
                    score -= 80.0
                elif distance <= 3:
                    score -= 22.0
                elif distance <= 4:
                    score -= 6.0
                active_ghost_nearby |= distance < 6

        # Viên sức mạnh có giá trị hơn khi có ma nguy hiểm ở gần.
        score -= 5.0 * len(capsules)
        if capsules and active_ghost_nearby:
            capsule_distance = min(manhattanDistance(position, p) for p in capsules)
            score += 18.0 / (capsule_distance + 1.0)

        # Hạn chế đứng yên khi còn hành động có ích.
        if action == Directions.STOP:
            score -= 12.0

        return score


def scoreEvaluationFunction(currentGameState: GameState):
    """Hàm đánh giá mặc định cho các thuật toán tìm kiếm đối kháng."""
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """Lớp cơ sở cho ba tác nhân Minimax, Alpha-Beta và Expectimax."""

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman luôn có chỉ số tác nhân bằng 0.
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """Q2: Minimax với nhiều ma; mỗi con ma tương ứng một tầng MIN."""

    def getAction(self, gameState: GameState):
        num_agents = gameState.getNumAgents()
        evaluate = self.evaluationFunction
        max_depth = self.depth

        def value(state, agent, depth):
            # Chỉ tăng độ sâu khi hết lượt tất cả ma và trở lại lượt Pacman.
            if depth == max_depth or state.isWin() or state.isLose():
                return evaluate(state)
            actions = state.getLegalActions(agent)
            if not actions:
                return evaluate(state)

            next_agent = (agent + 1) % num_agents
            next_depth = depth + (next_agent == 0)
            if agent == 0:
                result = float('-inf')
                for action in actions:
                    child = state.generateSuccessor(agent, action)
                    result = max(result, value(child, next_agent, next_depth))
                return result

            result = float('inf')
            for action in actions:
                child = state.generateSuccessor(agent, action)
                result = min(result, value(child, next_agent, next_depth))
            return result

        # Giữ nguyên thứ tự hành động: autograder kiểm tra các trạng thái được mở rộng.
        if max_depth <= 0 or gameState.isWin() or gameState.isLose():
            return Directions.STOP
        actions = gameState.getLegalActions(0)
        if not actions:
            return Directions.STOP

        next_agent = 1 % num_agents
        next_depth = int(next_agent == 0)
        best_action, best_value = actions[0], float('-inf')
        for action in actions:
            child = gameState.generateSuccessor(0, action)
            score = value(child, next_agent, next_depth)
            if score > best_value:
                best_action, best_value = action, score
        return best_action


class AlphaBetaAgent(MultiAgentSearchAgent):
    """Q3: Minimax có cắt tỉa Alpha-Beta (không cắt tỉa khi bằng nhau)."""

    def getAction(self, gameState: GameState):
        num_agents = gameState.getNumAgents()
        evaluate = self.evaluationFunction
        max_depth = self.depth

        def value(state, agent, depth, alpha, beta):
            if depth == max_depth or state.isWin() or state.isLose():
                return evaluate(state)
            actions = state.getLegalActions(agent)
            if not actions:
                return evaluate(state)

            next_agent = (agent + 1) % num_agents
            next_depth = depth + (next_agent == 0)

            if agent == 0:
                result = float('-inf')
                for action in actions:
                    child = state.generateSuccessor(agent, action)
                    result = max(result, value(child, next_agent, next_depth, alpha, beta))
                    # Chỉ cắt khi > beta; KHÔNG cắt khi bằng beta (quy định của Berkeley).
                    if result > beta:
                        return result
                    alpha = max(alpha, result)
                return result

            result = float('inf')
            for action in actions:
                child = state.generateSuccessor(agent, action)
                result = min(result, value(child, next_agent, next_depth, alpha, beta))
                # Tương tự, chỉ cắt khi < alpha; KHÔNG cắt khi bằng nhau.
                if result < alpha:
                    return result
                beta = min(beta, result)
            return result

        if max_depth <= 0 or gameState.isWin() or gameState.isLose():
            return Directions.STOP
        actions = gameState.getLegalActions(0)
        if not actions:
            return Directions.STOP

        next_agent = 1 % num_agents
        next_depth = int(next_agent == 0)
        best_action, best_value = actions[0], float('-inf')
        alpha, beta = float('-inf'), float('inf')

        # KHÔNG đổi thứ tự nước đi; truyền alpha giữa các nhánh tại gốc.
        for action in actions:
            child = gameState.generateSuccessor(0, action)
            score = value(child, next_agent, next_depth, alpha, beta)
            if score > best_value:
                best_action, best_value = action, score
            alpha = max(alpha, best_value)
        return best_action


class ExpectimaxAgent(MultiAgentSearchAgent):
    """Q4: Pacman là nút MAX; mỗi ma là nút CHANCE xác suất đều."""

    def getAction(self, gameState: GameState):
        num_agents = gameState.getNumAgents()
        evaluate = self.evaluationFunction
        max_depth = self.depth

        def value(state, agent, depth):
            if depth == max_depth or state.isWin() or state.isLose():
                return evaluate(state)
            actions = state.getLegalActions(agent)
            if not actions:
                return evaluate(state)

            next_agent = (agent + 1) % num_agents
            next_depth = depth + (next_agent == 0)
            if agent == 0:
                result = float('-inf')
                for action in actions:
                    child = state.generateSuccessor(agent, action)
                    result = max(result, value(child, next_agent, next_depth))
                return result

            # Ma chọn ngẫu nhiên đều giữa các nước hợp lệ, không lấy MIN.
            total = 0.0
            for action in actions:
                child = state.generateSuccessor(agent, action)
                total += value(child, next_agent, next_depth)
            return total / len(actions)

        if max_depth <= 0 or gameState.isWin() or gameState.isLose():
            return Directions.STOP
        actions = gameState.getLegalActions(0)
        if not actions:
            return Directions.STOP

        next_agent = 1 % num_agents
        next_depth = int(next_agent == 0)
        best_action, best_value = actions[0], float('-inf')
        for action in actions:
            child = gameState.generateSuccessor(0, action)
            score = value(child, next_agent, next_depth)
            if score > best_value:
                best_action, best_value = action, score
        return best_action


def betterEvaluationFunction(currentGameState: GameState):
    """Q5: Chấm điểm trạng thái từ thức ăn, viên sức mạnh và nguy cơ từ ma.

    Dùng BFS có bộ nhớ đệm theo bố cục và vị trí để đo đúng đường đi
    giữa các bức tường, đồng thời tránh duyệt lại bản đồ tại mỗi nút lá.
    """
    score = float(currentGameState.getScore())
    if currentGameState.isWin():
        return score + 1000000.0
    if currentGameState.isLose():
        return score - 1000000.0

    position = currentGameState.getPacmanPosition()
    px, py = position
    food_positions = currentGameState.getFood().asList()
    capsules = currentGameState.getCapsules()
    distances = _distancesFrom(position, currentGameState.getWalls())

    # Trừ điểm theo số thức ăn còn lại để Pacman chủ động dọn bản đồ.
    score -= 25.0 * len(food_positions)
    if food_positions:
        # Khoảng cách mê cung chuẩn, tra cứu O(1) cho mỗi viên thức ăn.
        closest = float('inf')
        density = 0.0
        for food_pos in food_positions:
            distance = distances.get(food_pos, float('inf'))
            if distance < closest:
                closest = distance
            if distance != float('inf'):
                density += 1.0 / (distance + 1.0)
        if closest != float('inf'):
            score -= 1.0 * closest
            score += 12.0 / (closest + 1.0) + 1.8 * density

    # Ưu tiên viên sức mạnh khi ma nguy hiểm xuất hiện gần Pacman.
    score -= 35.0 * len(capsules)
    active_ghost_nearby = False
    for ghost in currentGameState.getGhostStates():
        gx, gy = ghost.getPosition()
        distance = abs(px - gx) + abs(py - gy)
        scared_time = ghost.scaredTimer

        if scared_time > distance + 1:
            # Chỉ săn ma khi hiệu lực của viên sức mạnh đủ dài.
            score += 450.0 / (distance + 1.0)
        else:
            active_ghost_nearby |= distance < 6
            if distance <= 1:
                score -= 300.0
            elif distance <= 2:
                score -= 100.0
            elif distance <= 3:
                score -= 32.0
            elif distance <= 4:
                score -= 10.0

    if capsules and active_ghost_nearby:
        nearest_capsule = min(manhattanDistance(position, c) for c in capsules)
        score += 25.0 / (nearest_capsule + 1.0)

    return score


# Giữ bí danh better để chọn evalFn=better từ dòng lệnh.
better = betterEvaluationFunction

