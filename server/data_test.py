GET_LIST_AUTHORS = [ 
  { 
     'author_id':1,
     'books':[ 
        { 
           'book_id':1,
           'count_marks':0,
           'description':'Book',
           'name':'Default',
           'rating':0.0
        }
     ],
     'name':'Default',
     'sername':'Author'
  },
  { 
     'author_id':2,
     'books':[ 
        { 
           'book_id':1,
           'count_marks':0,
           'description':'Book',
           'name':'Default',
           'rating':0.0
        },
        { 
           'book_id':2,
           'count_marks':0,
           'description':'Book',
           'name':'Default',
           'rating':0.0
        },
        { 
           'book_id':3,
           'count_marks':0,
           'description':'Book',
           'name':'Default',
           'rating':0.0
        },
        { 
           'book_id':4,
           'count_marks':0,
           'description':'Book',
           'name':'Default',
           'rating':0.0
        },
        { 
           'book_id':5,
           'count_marks':0,
           'description':'Book',
           'name':'Default',
           'rating':0.0
        }
     ],
     'name':'Default',
     'sername':'Author'
  },
  { 
     'author_id':3,
     'books':[ 

     ],
     'name':'Default',
     'sername':'Author'
  }
]


DATA_GET_AUTHOR_BY_ID = {
    'author_id': 1,
    'books': [{
        'book_id': 1,
        'count_marks': 0,
        'description': 'Book',
        'name': 'Default',
        'rating': .0
    }],
    'name': 'Default',
    'sername': 'Author'
}


DATA_TEST_AUTHORS_PAGINATION = { 
  'has_next':True,
  'has_prev':True,
  'next_num':4,
  'pages':4,
  'prev_num':2
}


DATA_TEST_BOOKS_PAGINATION = { 
  'has_next':True,
  'has_prev':True,
  'next_num':3,
  'pages':5,
  'prev_num':1
}


DATA_GET_BOOK_BY_ID = { 
   'authors':[ 
      { 
         'author_id':1,
         'name':'Default',
         'sername':'Author'
      },
      { 
         'author_id':2,
         'name':'Default',
         'sername':'Author'
      }
   ],
   'book_id':1,
   'count_marks':0,
   'description':'Book',
   'name':'Default',
   'rating':0.0
}


DATA_GET_BOOK_LIST = [{ 
    'authors':[{ 
        'author_id':2,
        'name':'Default',
        'sername':'Author'
    }],
    'book_id': 7,
    'count_marks': 0,
    'description': 'Book',
    'name':'Default',
    'rating':0.0
},
{ 
    'authors':[{ 
        'author_id':2,
        'name':'Default',
        'sername':'Author'
    }
    ],
    'book_id':8,
    'count_marks':0,
    'description':'Book',
    'name':'Default',
    'rating':0.0
},
{ 
    'authors':[{ 
        'author_id':2,
        'name':'Default',
        'sername':'Author'
    }],
    'book_id':9,
    'count_marks':0,
    'description':'Book',
    'name':'Default',
    'rating':0.0
}]

