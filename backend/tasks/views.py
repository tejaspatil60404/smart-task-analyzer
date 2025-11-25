from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .serializers import TaskInputSerializer
from .scoring import score_tasks


@api_view(["POST"])
def analyze_tasks(request):

    serializer = TaskInputSerializer(data=request.data, many=True)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    tasks = serializer.validated_data

    # Call your scoring function
    scored = score_tasks(tasks)

    return Response(scored, status=200)

@api_view(["POST"])
def suggest_tasks(request):


    serializer = TaskInputSerializer(data=request.data, many=True)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    tasks = serializer.validated_data

    # Score tasks using the simple scoring system
    scored = score_tasks(tasks)

    # Pick top 3
    top_tasks = scored[:3]

    # Add short explanation: why chosen
    for task in top_tasks:
        task["suggest_reason"] = f"Selected because it has a high priority score of {task['score']}."

    return Response(top_tasks, status=200)
