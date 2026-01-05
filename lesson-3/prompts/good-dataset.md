I am building a demo multi-agent AI application for runners. It can answer questions about:

- Running shoe and clothing recommendations
- Training plans for different types of running
- Upcoming races
- Recovery
- Nutrition

For shoes and clothing, the brands that it knows about are made up brands including Nyxon Running Co., Adizone Performance, Hokaro Lab, Saukion Athletics, and Brukes RunLab.

For upcoming races, there are all kinds from trail to road, and distances from 5K to a marathon.

I need to build a dataset that represents the kinds of questions that a user might ask this application to run a series of tests. I need:

- 100 test cases
- Each test case containing either a single question, or one or more relevant follow up questions

The output should be in JSON in the following format:

```json
{
  [
    { "input": [
        "Question"
      ]
    },
    { "input": [
        "Question",
        "Follow up question"
      ]
    }  
  ]
}
```

Make a plan to produce these 100 records, then generate them as JSON.
