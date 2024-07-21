from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from .serializers import PredictionSerializer
import pandas as pd
import pickle
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

path= 'model/Student_score_model.sav'
model=pickle.load(open(path,'rb'))
class PredictView(APIView):
    serializer_class = PredictionSerializer

    def predict_score(self,df_input):
        df = df_input.copy()
        df.columns = df.columns.str.lower().str.replace(' ', '_')
        df['extracurricular_activities'] = df['extracurricular_activities'].apply(
            lambda x: 1 if x.lower() == 'yes' else 0)
        if len(df.columns) == 5:
            pred = pd.Series(model.predict(df))
            df['result'] = pred.apply(lambda x: 100.0 if round(x, 0) > 100 else 0.0 if round(x, 0) < 0 else round(x, 0))
            return df['result'].to_list()
        elif len(df.columns) == 6:
            df.drop(columns='performance_index', inplace=True)
            pred = pd.Series(model.predict(df))
            df['result'] = pred.apply(lambda x: 100.0 if round(x, 0) > 100 else 0.0 if round(x, 0) < 0 else round(x, 0))
            return df['result'].to_list()
        else:
            return list()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        df= pd.DataFrame({
            'hours_studied': serializer.validated_data['hours_studied'],
            'previous_scores': serializer.validated_data['previous_scores'],
            'extracurricular_activities': serializer.validated_data['extracurricular_activities'],
            'sleep_hours': serializer.validated_data['sleep_hours'],
            'sample_question_papers_practiced': serializer.validated_data['sample_question_papers_practiced'],
        }, index=[0])
        result=self.predict_score(df)
        return Response(data={'predicted_score':result[0]}, status=status.HTTP_200_OK)





